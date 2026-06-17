"""End-to-end Agentic Cleanroom pipeline (front: spec -> dependency -> planning).

Runs the front of the pipeline on a single SRS document and saves the enriched IR:

    SRS.xml
      -> [1] Spec        parse + FR/NFR classification     [parse: deterministic, classify: LLM]
      -> [2] Dependency  nested graph (feature + FR level)  [regex deterministic, inner: optional LLM]
      -> [3] Planning    one contract per FR                [LLM: signature/docstring/layer]
      -> [4] Code / [5] Test / [6] Certification            [LLM — see note below]

Stage 1 parses deterministically (IDs/grouping never come from the LLM), then makes one
LLM call PER FEATURE to label each requirement FR or NFR (NFRs carry a category + rationale).
Stage 2 builds an OUTER feature-level DAG and an INNER per-feature FR graph; cross-reference
detection is deterministic, and when an LLM is supplied the inner level also infers semantic
FR->FR prerequisites. Stage 3 walks the FRs in dependency order and emits a CONTRACT per FR
(function signature + docstring + MVC-aware file_path), one LLM call per feature.

Stages 4-6 (Code, Test, Certification) consume the planner's per-FR contracts: Code turns
each contract into a file (one LLM call per contract), Test derives black-box cases from the
spec, and Certification scores pass@k. They run on a real-model run; with --stub-llm the
runner stops after Planning.

Token-free runs: pass --stub-llm (or --no-llm) to drive spec, dependency and planning with
deterministic stub LLMs — the whole front pipeline runs with ZERO tokens and no API key.

Usage:
    uv run python run_pipeline.py "data/srs/2005 - phin.xml"              # real gpt-4o-mini
    uv run python run_pipeline.py "data/srs/2005 - phin.xml" --stub-llm   # zero tokens, no key
    uv run python run_pipeline.py "data/srs/2005 - phin.xml" --no-llm     # same: stub front

A real run needs OPENAI_API_KEY in .env; without it (and without a stub flag) the runner
falls back to the stub LLMs so the front pipeline still completes.
"""

import argparse
import json
import os
import re
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


def _banner(step: str, title: str) -> None:
    print(f"\n{'=' * 70}\n  {step}  {title}\n{'=' * 70}")


# --------------------------------------------------------------------------
# Deterministic stub LLMs — let the front pipeline run with ZERO tokens.
# They parse the "[id] text" lines out of the rendered prompt and return the
# same structured objects the real model would, using simple keyword heuristics.
# --------------------------------------------------------------------------
_PROMPT_REQ = re.compile(r"(?m)^- \[([^\]]+)\]\s*(.*)$")
_NFR_HINTS = ("secur", "privacy", "privat", "performan", "availab", "reliab", "robust",
              "maintain", "usab", "backup", "polic", "standard", "encrypt", "protect", "unauthorized")
# Capability verbs: if a requirement DELIVERS one of these, it is functional even when its
# text also mentions a quality word (the anti-keyword rule, in heuristic form).
_FR_VERBS = ("captur", "collect", "creat", "send", "store", "link", "produc", "record",
             "exchang", "assign", "generat", "support", "provid", "accept", "aggregat",
             "track", "publish", "import", "export", "comput", "process", "display", "print")
_MODEL_HINTS = ("data", "store", "record", "persist", "captur", "schema", "entit")
_VIEW_HINTS = ("report", "visual", "display", "print", "screen", "chart", "graph", "present")

_NFR_RATIONALE = {
    "security": "Protects the system and its data from unauthorized access, corruption, and sabotage.",
    "privacy": "Keeps sensitive personal and investigation information from unauthorized use.",
    "availability": "Keeps the system and its data usable when needed, including after disruption.",
    "performance": "Bounds responsiveness or throughput so the system performs adequately under load.",
    "robustness": "Keeps the system behaving correctly under error, edge, or failure conditions.",
    "maintainability": "Keeps the system adaptable and its data interpretable over time.",
    "usability": "Ensures the system can be operated effectively by its intended users.",
    "other": "A quality constraint the implementation must satisfy beyond its core behavior.",
}


def _nfr_category(text: str) -> str:
    t = text.lower()
    for key, cat in (("secur", "security"), ("privacy", "privacy"), ("privat", "privacy"),
                     ("performan", "performance"), ("availab", "availability"), ("backup", "availability"),
                     ("reliab", "robustness"), ("robust", "robustness"), ("maintain", "maintainability"),
                     ("usab", "usability"), ("standard", "maintainability")):
        if key in t:
            return cat
    return "other"


class StubSpecLLM:
    """Stands in for the spec classifier. Honors the anti-keyword rule: a requirement that
    DELIVERS a capability (capture/create/send/...) stays FR even if its text mentions a
    quality word; only no-capability + quality-hint requirements become NFRs."""

    def with_structured_output(self, _model):
        from src.cleanroom.agents.spec_agent.schema.ir import (
            FeatureClassification, RequirementClassification)

        class _S:
            def invoke(self, prompt):
                out = []
                for rid, text in _PROMPT_REQ.findall(prompt):
                    low = text.lower()
                    is_nfr = any(h in low for h in _NFR_HINTS) and not any(v in low for v in _FR_VERBS)
                    if is_nfr:
                        cat = _nfr_category(text)
                        out.append(RequirementClassification(
                            id=rid, kind="NFR", category=cat, rationale=_NFR_RATIONALE[cat]))
                    else:
                        out.append(RequirementClassification(id=rid, kind="FR"))
                return FeatureClassification(classifications=out)

        return _S()


_DEP_CONSUMER = ("link", "store", "updat", "receiv", "process", "referenc", "associat")
_DEP_PRODUCER = ("creat", "assign", "defin", "develop", "generat")
_DEP_NOUNS = ("request", "specimen", "result", "event", "case", "questionnaire", "identifier", "record")


class StubDepLLM:
    """Stands in for the inner semantic pass: links a requirement that consumes a thing
    (link/store/...) to one that produces it (create/assign/...) when they share a noun."""

    def with_structured_output(self, _model):
        from src.cleanroom.agents.dependency.schema.graph import FeatureFRDeps, FRDependency

        class _S:
            def invoke(self, prompt):
                reqs = _PROMPT_REQ.findall(prompt)
                deps = []
                for sid, stext in reqs:
                    sl = stext.lower()
                    if not any(v in sl for v in _DEP_CONSUMER):
                        continue
                    s_nouns = {n for n in _DEP_NOUNS if n in sl}
                    if not s_nouns:
                        continue
                    prereqs = [tid for tid, ttext in reqs
                               if tid != sid and any(v in ttext.lower() for v in _DEP_PRODUCER)
                               and s_nouns & {n for n in _DEP_NOUNS if n in ttext.lower()}]
                    if prereqs:
                        deps.append(FRDependency(id=sid, prerequisite_ids=prereqs))
                return FeatureFRDeps(dependencies=deps)

        return _S()


class StubPlanLLM:
    """Stands in for the planner: a generic signature/docstring and a keyword-based layer."""

    def with_structured_output(self, _model):
        from src.cleanroom.agents.planning.schema.plan import ArgDoc, FeaturePlan, FRPlan

        class _S:
            def invoke(self, prompt):
                plans = []
                for rid, text in _PROMPT_REQ.findall(prompt):
                    low = text.lower()
                    layer = ("view" if any(h in low for h in _VIEW_HINTS)
                             else "model" if any(h in low for h in _MODEL_HINTS)
                             else "controller")
                    plans.append(FRPlan(
                        id=rid,
                        signature=f"def fr_{rid.replace('.', '_')}(data: dict) -> dict:",
                        summary=f"Implements requirement {rid}: {text[:80]}",
                        args=[ArgDoc(name="data", description="Input payload for this requirement.")],
                        returns="The result of processing the requirement.",
                        mvc_layer=layer))
                return FeaturePlan(plans=plans)

        return _S()


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


def run(srs_path: Path, output_dir: Path, use_llm: bool, certify: bool = False, samples: int = 5,
        spec_llm=None, plan_llm=None, dep_llm=None) -> tuple[dict, dict]:
    stages: list = []
    metrics: dict = {"srs": srs_path.name, "stages": stages}

    # --- Stage 1: Spec (deterministic parse + LLM FR/NFR classification) ------
    _banner("[1]", "Spec Agent — parsing the SRS + classifying FR/NFR")
    spec = SpecAgent()
    if spec_llm is not None:
        spec.llm = spec_llm  # stub injection for token-free runs
    ir_obj = _timed("spec_parse", stages, lambda: spec.run(srs_path, output_dir=output_dir))
    ir = ir_obj.model_dump()
    ir = _timed("spec_classify", stages, lambda: spec.enrich(ir, output_dir=output_dir))
    n_fr = sum(len(f["functional_requirements"]) for f in ir["features"])
    n_nfr = sum(len(f.get("non_functional_requirements", [])) for f in ir["features"])
    print(f"Project   : {ir['project_name']}")
    print(f"Features  : {len(ir['features'])}  (FR={n_fr}, NFR={n_nfr})")

    # --- Stage 2: Dependency (nested; inner semantic pass when an LLM is provided) ---
    _banner("[2]", "Dependency Agent — building the nested dependency graph")
    ir = _timed("dependency", stages, lambda: DependencyAnalyzer(llm=dep_llm).enrich(ir, output_dir=output_dir))
    graph = ir["dependency_graph"]
    print(f"Outer nodes : {len(graph['nodes'])}  edges: {len(graph['edges'])}")
    print(f"Build order : {' -> '.join(graph['build_order']) or '(none)'}")
    print(f"Cycles      : {graph['cycles'] or 'none'}")
    inner_edges = sum(len(f.get("fr_edges", [])) for f in ir["features"])
    inner_cycles = sum(len(f.get("fr_cycles", [])) for f in ir["features"])
    print(f"Inner (FR)  : {inner_edges} edge(s), {inner_cycles} cycle(s) across features")

    # --- Stage 3: Planning (per-FR contracts) --------------------------------
    _banner("[3]", "Planning Agent — generating per-FR contracts (signature + docstring + path)")
    ir = _timed("planning", stages, lambda: PlanningAgent(llm=plan_llm).enrich(ir, output_dir=output_dir))
    contracts = ir["planning"]["contracts"]
    print(f"Contracts   : {len(contracts)}  (in dependency order)")
    for c in contracts[:12]:
        print(f"  [{c['fr_id']}] ({c['mvc_layer']}) {c['signature']}")
        print(f"        -> {c['file_path']}   prereqs={c['prerequisite_fr_ids']}")
    if len(contracts) > 12:
        print(f"  … and {len(contracts) - 12} more (see {ir['project_name']}_planning.json)")

    # Stages 4-6 (Code/Test/Certification) consume the planner's per-FR contracts.
    # With the deterministic stubs there is no real model to generate code/tests, so the
    # front pipeline stops after planning.
    if not use_llm or not ir.get("planning", {}).get("contracts"):
        print("\n(Front pipeline complete: spec -> dependency -> planning. Code/Test/"
              "Certification are skipped — run with the real model, not --stub-llm.)")
        _finalize_metrics(metrics, stages)
        return ir, metrics

    # --- Stage 4: Code (LLM) -------------------------------------------------
    _banner("[4]", "Code Agent — generating MVC code from the spec")
    code_agent = CodeAgent()
    generated_code = _timed("code", stages, lambda: code_agent.generate(ir))
    ir = {**ir, "generated_code": generated_code.model_dump()}
    code_dir = output_dir / "generated" / ir["project_name"]
    written = CodeAgent.write_files(generated_code, code_dir)
    metrics["code"] = code_stats(ir["generated_code"])
    print(f"Wrote {len(written)} file(s); {metrics['code']['lines_of_code']} LOC "
          f"({metrics['code']['language']}); layers={metrics['code']['files_per_layer']}")

    # --- Stage 5: Test (LLM) -------------------------------------------------
    # The Test Agent reads only ir['features']; passing the full (code-bearing) IR
    # here does NOT break isolation — the agent structurally ignores generated_code.
    _banner("[5]", "Test Agent — deriving black-box tests from the spec")
    generated_tests = _timed("test", stages, lambda: TestAgent().generate(ir))
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
    parser.add_argument("--no-llm", action="store_true",
                        help="Run the front pipeline with deterministic stub LLMs (zero tokens, no key).")
    parser.add_argument("--certify", action="store_true", help="Also run the pass@k certification stage.")
    parser.add_argument("--samples", type=int, default=5, help="Code samples per feature for pass@k (default 5).")
    parser.add_argument("--stub-llm", action="store_true",
                        help="Run spec+dependency+planning with deterministic stub LLMs (zero tokens, no key).")
    args = parser.parse_args()

    if not args.srs_path.exists():
        parser.error(f"SRS file not found: {args.srs_path}")

    spec_llm = plan_llm = dep_llm = None
    # Spec (FR/NFR classification) and Planning (signatures) now need an LLM, so the
    # token-free path injects deterministic stubs across the front pipeline.
    stub = args.stub_llm or args.no_llm
    if not stub and not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set — falling back to stub LLMs (zero tokens).\n")
        stub = True

    if stub:
        spec_llm, plan_llm, dep_llm = StubSpecLLM(), StubPlanLLM(), StubDepLLM()
        use_llm = False  # Code/Test/Certification stay off (pending rewire onto contracts)
    else:
        from src.cleanroom.utils.llm_client import get_llm
        dep_llm = get_llm()  # enable the inner semantic dependency pass on real runs
        use_llm = True

    ir, metrics = run(args.srs_path, args.output_dir, use_llm, certify=args.certify, samples=args.samples,
                      spec_llm=spec_llm, plan_llm=plan_llm, dep_llm=dep_llm)
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
