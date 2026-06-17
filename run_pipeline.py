"""End-to-end Agentic Cleanroom pipeline.

Runs the full pipeline on a single SRS document and saves the enriched IR:

    SRS.xml
      -> [1] Spec        parse + FR/NFR classification     [parse: deterministic, classify: LLM]
      -> [2] Dependency  nested graph (feature + FR level)  [regex deterministic, inner: LLM semantic]
      -> [3] Planning    one contract per FR                [LLM: signature/docstring/layer]
      -> [4] Code        MVC source files                   [LLM: one call per contract]
      -> [5] Test        black-box test cases               [LLM: one call per feature]
      -> [6] Certification  pass@k scoring                  [LLM, opt-in via --certify]

Requires OPENAI_API_KEY in .env.

Usage:
    uv run python run_pipeline.py "data/srs/2005 - phin.xml"
    uv run python run_pipeline.py "data/srs/2005 - phin.xml" --certify
    uv run python run_pipeline.py "data/srs/2005 - phin.xml" --certify --samples 10
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from src.cleanroom.agents.evaluation.agent import CertificationAgent
from src.cleanroom.agents.code.agent import CodeAgent
from src.cleanroom.agents.dependency.agent import DependencyAnalyzer
from src.cleanroom.agents.planning.agent import PlanningAgent
from src.cleanroom.agents.spec_agent.agent import SpecAgent
from src.cleanroom.agents.test.agent import TestAgent
from src.cleanroom.llms.callbacks.metric import GLOBAL_METRICS
from src.cleanroom.utils.code_stats import code_stats
from src.cleanroom.utils.cost import estimate_cost
from src.cleanroom.utils.llm_client import get_llm


def _banner(step: str, title: str) -> None:
    print(f"\n{'=' * 70}\n  {step}  {title}\n{'=' * 70}")


def _timed(name: str, stages: list, fn):
    """Run fn(), recording (and printing) its wall-clock time and LLM tokens consumed."""
    in0, out0, calls0 = GLOBAL_METRICS.snapshot()
    t0 = time.perf_counter()
    result = fn()
    seconds = time.perf_counter() - t0
    in1, out1, calls1 = GLOBAL_METRICS.snapshot()
    calls = calls1 - calls0
    stages.append(
        {
            "name": name,
            "seconds": round(seconds, 3),
            "input_tokens": in1 - in0,
            "output_tokens": out1 - out0,
            "calls": calls,
        }
    )
    extra = f"  ·  {(in1 - in0) + (out1 - out0):,} tokens, {calls} call(s)" if calls else ""
    print(f"  ⏱  done in {seconds:.2f}s{extra}")
    return result


def _finalize_metrics(metrics: dict, stages: list) -> None:
    in_tot, out_tot, calls = GLOBAL_METRICS.snapshot()
    model = GLOBAL_METRICS.model or "gpt-4o-mini"
    metrics["model"] = model
    metrics["total_seconds"] = round(sum(s["seconds"] for s in stages), 3)
    metrics["tokens"] = {"input": in_tot, "output": out_tot, "total": in_tot + out_tot, "calls": calls}
    metrics["cost_usd"] = round(estimate_cost(model, in_tot, out_tot), 6)


def run(srs_path: Path, output_dir: Path, certify: bool = False, samples: int = 5) -> tuple[dict, dict]:
    stages: list = []
    metrics: dict = {"srs": srs_path.name, "stages": stages}
    llm = get_llm()

    # --- Stage 1: Spec (deterministic parse + LLM FR/NFR classification) ------
    _banner("[1]", "Spec Agent — parsing the SRS + classifying FR/NFR")
    spec = SpecAgent()
    ir_obj = _timed("spec_parse", stages, lambda: spec.run(srs_path, output_dir=output_dir))
    ir = ir_obj.model_dump()
    ir = _timed("spec_classify", stages, lambda: spec.enrich(ir, output_dir=output_dir))
    n_fr = sum(len(f["functional_requirements"]) for f in ir["features"])
    n_nfr = sum(len(f.get("non_functional_requirements", [])) for f in ir["features"])
    print(f"Project   : {ir['project_name']}")
    print(f"Features  : {len(ir['features'])}  (FR={n_fr}, NFR={n_nfr})")

    # --- Stage 2: Dependency (nested; LLM infers semantic FR->FR edges) -------
    _banner("[2]", "Dependency Agent — building the nested dependency graph")
    ir = _timed("dependency", stages, lambda: DependencyAnalyzer(llm=llm).enrich(ir, output_dir=output_dir))
    graph = ir["dependency_graph"]
    print(f"Outer nodes : {len(graph['nodes'])}  edges: {len(graph['edges'])}")
    print(f"Build order : {' -> '.join(graph['build_order']) or '(none)'}")
    print(f"Cycles      : {graph['cycles'] or 'none'}")
    inner_edges = sum(len(f.get("fr_edges", [])) for f in ir["features"])
    inner_cycles = sum(len(f.get("fr_cycles", [])) for f in ir["features"])
    print(f"Inner (FR)  : {inner_edges} edge(s), {inner_cycles} cycle(s) across features")

    # --- Stage 3: Planning (per-FR contracts) --------------------------------
    _banner("[3]", "Planning Agent — generating per-FR contracts (signature + docstring + path)")
    ir = _timed("planning", stages, lambda: PlanningAgent(llm=llm).enrich(ir, output_dir=output_dir))
    contracts = ir["planning"]["contracts"]
    print(f"Contracts   : {len(contracts)}  (in dependency order)")
    for c in contracts[:12]:
        print(f"  [{c['fr_id']}] ({c['mvc_layer']}) {c['signature']}")
        print(f"        -> {c['file_path']}   prereqs={c['prerequisite_fr_ids']}")
    if len(contracts) > 12:
        print(f"  … and {len(contracts) - 12} more (see {ir['project_name']}_planning.json)")

    # --- Stage 4: Code (LLM) -------------------------------------------------
    _banner("[4]", "Code Agent — generating MVC code from the spec")
    code_agent = CodeAgent(llm=llm)
    generated_code = _timed("code", stages, lambda: code_agent.generate(ir))
    ir = {**ir, "generated_code": generated_code.model_dump()}
    code_dir = output_dir / "generated" / ir["project_name"]
    written = CodeAgent.write_files(generated_code, code_dir)
    metrics["code"] = code_stats(ir["generated_code"])
    print(f"Wrote {len(written)} file(s); {metrics['code']['lines_of_code']} LOC "
          f"({metrics['code']['language']}); layers={metrics['code']['files_per_layer']}")

    # --- Stage 5: Test (LLM) -------------------------------------------------
    # The Test Agent reads only ir['features']; the generated_code in the IR is
    # structurally ignored — isolation is preserved.
    _banner("[5]", "Test Agent — deriving black-box tests from the spec")
    generated_tests = _timed("test", stages, lambda: TestAgent(llm=llm).generate(ir))
    ir = {**ir, "generated_tests": generated_tests.model_dump()}
    tests_dir = output_dir / "generated" / ir["project_name"] / "tests"
    TestAgent.write_files(generated_tests, tests_dir)
    total_cases = sum(len(f.cases) for f in generated_tests.features)
    metrics["tests"] = {"features": len(generated_tests.features), "cases": total_cases}
    print(f"{len(generated_tests.features)} feature(s), {total_cases} test case(s).")

    # --- Stage 6: Certification (LLM, optional) ------------------------------
    if certify:
        _banner("[6]", f"Certification Agent — pass@k (n={samples} samples)")
        cert = _timed("certification", stages, lambda: CertificationAgent(n=samples).run(ir))
        ir = {**ir, "certification": cert.model_dump()}
        metrics["certification"] = {"n": cert.n, "k_values": cert.k_values, "aggregate_pass_at": cert.aggregate_pass_at}
        for k, v in cert.aggregate_pass_at.items():
            print(f"  {k}: {v:.3f}")

    _finalize_metrics(metrics, stages)
    return ir, metrics


def write_run_report(metrics: dict, dest: Path) -> None:
    lines = [
        "# Run report",
        "",
        f"_SRS: {metrics['srs']} · model: {metrics.get('model', 'n/a')}_",
        "",
        "## Timing & tokens (per stage)",
        "",
        "| stage | seconds | input tok | output tok | calls |",
        "|---|---|---|---|---|",
    ]
    for s in metrics["stages"]:
        lines.append(f"| {s['name']} | {s['seconds']:.2f} | {s['input_tokens']:,} | {s['output_tokens']:,} | {s['calls']} |")
    tok = metrics.get("tokens", {"input": 0, "output": 0, "total": 0, "calls": 0})
    lines += [
        f"| **total** | **{metrics.get('total_seconds', 0):.2f}** | **{tok['input']:,}** | **{tok['output']:,}** | **{tok['calls']}** |",
        "",
        "## Tokens & cost",
        "",
        f"- total tokens: {tok['total']:,}  (input {tok['input']:,} / output {tok['output']:,})",
        f"- LLM calls: {tok['calls']}",
        f"- estimated cost: ${metrics.get('cost_usd', 0):.4f}",
    ]
    if metrics.get("code"):
        c = metrics["code"]
        stack = ", ".join(c["third_party_libraries"]) or "Python standard library only"
        lines += [
            "",
            "## Generated code",
            "",
            f"- language: {c['language']}",
            f"- files: {c['files']} · lines of code: {c['lines_of_code']:,}",
            f"- files per layer: {c['files_per_layer']}",
            f"- tech stack: {stack}",
        ]
    if metrics.get("tests"):
        t = metrics["tests"]
        lines += ["", "## Generated tests", "", f"- features: {t['features']} · test cases: {t['cases']}"]
    if metrics.get("certification"):
        cert = metrics["certification"]
        lines += ["", "## Certification (pass@k)", "", f"- samples n={cert['n']}"]
        lines += [f"- {k}: {v:.3f}" for k, v in cert["aggregate_pass_at"].items()]
    dest.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full Agentic Cleanroom pipeline on an SRS document.")
    parser.add_argument("srs_path", type=Path, help="Path to the SRS XML document")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Where to write artifacts")
    parser.add_argument("--certify", action="store_true", help="Also run the pass@k certification stage.")
    parser.add_argument("--samples", type=int, default=5, help="Code samples per feature for pass@k (default 5).")
    args = parser.parse_args()

    if not args.srs_path.exists():
        parser.error(f"SRS file not found: {args.srs_path}")

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY is not set. Add it to your .env file.")
        sys.exit(1)

    ir, metrics = run(args.srs_path, args.output_dir, certify=args.certify, samples=args.samples)
    ir = {**ir, "metrics": metrics}

    dest = args.output_dir / f"{args.srs_path.stem}_full_ir.json"
    dest.write_text(json.dumps(ir, indent=2))
    report = args.output_dir / f"{args.srs_path.stem}_run_report.md"
    write_run_report(metrics, report)

    _banner("DONE", "Run complete")
    print(f"IR        : {dest}")
    print(f"Report    : {report}")
    per_stage = "   ".join(f"{s['name']}={s['seconds']:.1f}s" for s in metrics["stages"] if s["seconds"] >= 0.01)
    print(f"Per stage : {per_stage}")
    print(f"Time      : {metrics['total_seconds']:.2f}s   Tokens: {metrics['tokens']['total']:,}   Cost: ${metrics['cost_usd']:.4f}")


if __name__ == "__main__":
    main()
