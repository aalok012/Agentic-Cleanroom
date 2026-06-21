"""End-to-end Agentic Cleanroom pipeline.

Runs the full pipeline on a single SRS document and saves the enriched IR:

    SRS.xml
      -> [1] Spec        FR parse + behavioral contracts    [parse: deterministic, contracts: LLM]
      -> [2] Dependency  nested graph (feature + FR level)  [regex deterministic, inner: LLM semantic]
      -> [3] Planning    impl metadata per FR contract      [LLM: signature/layer; docstring deterministic]
      -> [4] Code        MVC source files                   [LLM: one call per contract]
      -> [4b] Verification  contract conformance + revise   [LLM, opt-in via --verify]
      -> [5] Test        black-box test cases               [LLM: one call per feature]
      -> [6] Certification  pass@k scoring                  [executable oracle, opt-in via --certify]

Requires OPENAI_API_KEY in .env.

Usage:
    uv run python run_pipeline.py "data/srs/dineout_srs.xml"
    uv run python run_pipeline.py "data/srs/dineout_srs.xml" --verify --verify-rounds 1
    uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --samples 1
    uv run python run_pipeline.py "data/srs/dineout_srs.xml" --verify --verify-rounds 1 --certify --samples 3
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
from src.cleanroom.agents.dafny.agent import DafnyAgent
from src.cleanroom.agents.dependency.agent import DependencyAnalyzer
from src.cleanroom.agents.planning.agent import PlanningAgent
from src.cleanroom.agents.spec_agent.agent import SpecAgent
from src.cleanroom.agents.test.agent import TestAgent
from src.cleanroom.agents.verification.agent import VerificationAgent
from src.cleanroom.agents.verification.loop import generate_and_verify
from src.cleanroom.llms.callbacks.metric import GLOBAL_METRICS
from src.cleanroom.utils.code_stats import code_stats
from src.cleanroom.utils.cost import estimate_cost
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.lemmafit_project import compile_dafny_to_ts, scaffold_lemmafit_project
from src.cleanroom.utils.packager import build_runnable_package
from src.cleanroom.utils.stack_select import select_stack
from src.cleanroom.utils.ir import normalize_ir
from src.cleanroom.utils.run_record import make_run_id, record_run
from src.cleanroom.utils.usage_log import append_usage_log, metrics_from_globals

# The LemmaFit/Dafny stack needs a strong model — the spikes showed gpt-4o-mini/gpt-4o cannot
# discharge map-comprehension proofs, while gpt-4.1 verifies mutating CRUD features in a few rounds.
_DAFNY_MODEL = "gpt-4.1"


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


def run(
    srs_path: Path,
    output_dir: Path,
    certify: bool = False,
    samples: int = 5,
    stack: str = "python",
    verify: bool = False,
    verify_rounds: int = 2,
    verify_model: str = "gpt-4o-mini",
    verify_passes: int = 1,
) -> tuple[dict, dict]:
    stages: list = []
    run_config = {
        "certify": certify,
        "samples": samples,
        "verify": verify,
        "verify_rounds": verify_rounds,
        "verify_model": verify_model,
        "verify_passes": verify_passes,
    }
    metrics: dict = {"srs": srs_path.name, "stack": stack, "stages": stages, "config": run_config}
    llm = get_llm()

    # --- Stage 1: Spec (deterministic FR parse, then LLM behavioral contracts) -
    # The SRSReader extracts functional requirements only (section-aware, no LLM); the
    # contract phase then writes a design-by-contract spec per FR (one LLM call/feature).
    _banner("[1]", "Spec Agent — parsing the SRS (FR-only) and writing behavioral contracts")
    spec = SpecAgent(llm=llm)
    ir_obj = _timed("spec_parse", stages, lambda: spec.run(srs_path, output_dir=output_dir))
    ir = ir_obj.model_dump()
    ir = _timed("spec_contracts", stages,
                lambda: spec.synthesize_contracts(ir, output_dir=output_dir))
    n_fr = sum(len(f["functional_requirements"]) for f in ir["features"])
    print(f"Project   : {ir['project_name']}")
    print(f"Features  : {len(ir['features'])}  (FR={n_fr})")
    print(f"Contracts : {len(ir['contracts'])}")

    # --- Resolve the target stack (auto-select from the spec unless pinned) -----
    # Done here, after contracts exist, so the classifier can read preconditions. The
    # chosen stack drives planning signatures, codegen shape, packaging and certification.
    if stack == "auto":
        stack, reason = select_stack(ir)
        print(f"Stack     : {stack}  (auto-selected — {reason})")
    else:
        print(f"Stack     : {stack}  (pinned via --stack)")
    metrics["stack"] = stack
    ir["stack"] = stack

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
    ir = _timed("planning", stages, lambda: PlanningAgent(llm=llm, stack=stack).enrich(ir, output_dir=output_dir))
    contracts = ir["planning"]["contracts"]
    print(f"Contracts   : {len(contracts)}  (in dependency order)")
    for c in contracts[:12]:
        print(f"  [{c['fr_id']}] ({c['mvc_layer']}) {c['signature']}")
        print(f"        -> {c['file_path']}   prereqs={c['prerequisite_fr_ids']}")
    if len(contracts) > 12:
        print(f"  … and {len(contracts) - 12} more (see {ir['project_name']}_planning.json)")

    # --- LemmaFit/TypeScript stack: generate VERIFIED Dafny, then compile to TS -----
    # This stack replaces stages 4-6: the Dafny Agent casts each feature into a Dafny state
    # machine and PROVES it against the spec (formal verification is the certification);
    # certify additionally compiles the verified Dafny to a TypeScript client.
    if stack == "lemmafit":
        _banner("[4]", "Dafny Agent — generating VERIFIED Dafny (LemmaFit) from the spec")
        project_dir = output_dir / "generated" / ir["project_name"] / "lemmafit"
        # Skip npm install: verification + Dafny→TS compile use the global toolchain, not
        # node_modules (which is only needed to RUN the app). Run `npm install` in the project
        # manually if you later want `npm run dev`.
        proj = _timed("scaffold", stages,
                      lambda: scaffold_lemmafit_project(project_dir, install_deps=False))
        agent = DafnyAgent(proj, model=_DAFNY_MODEL)
        gen = _timed("dafny", stages, lambda: agent.generate(ir))
        (proj / "SPEC.yaml").write_text(gen.spec_yaml)
        ir = {**ir, "generated_dafny": gen.model_dump()}
        ntot, nver = len(gen.features), gen.n_verified
        print(f"Project   : {proj}")
        print(f"Verified  : {nver}/{ntot} features")
        for f in gen.features:
            print(f"  [{f.feature_id}] {'OK' if f.verified else 'XX'}  {f.module}  ({f.rounds} round(s))")
        metrics["dafny"] = {
            "model": _DAFNY_MODEL, "n_features": ntot, "n_verified": nver,
            "verification_rate": round(nver / ntot, 3) if ntot else 0.0,
            "features": [{"feature_id": f.feature_id, "module": f.module,
                          "verified": f.verified, "rounds": f.rounds} for f in gen.features],
        }
        if certify:
            _banner("[5]", "Compile — Dafny → TypeScript (dafny2js, best effort)")
            comp = _timed("compile", stages, lambda: compile_dafny_to_ts(proj, gen))
            metrics["compile"] = comp
            print(f"Compiled  : {len(comp['compiled'])}/{ntot} features to TypeScript")
            for c in comp.get("failed", []):
                print(f"  [{c['feature_id']}] not compiled: {c['reason'][:80]}")
        _finalize_metrics(metrics, stages)
        return ir, metrics

    # --- Stage 4: Code (LLM) + optional verification / executable fix ---------------
    _banner("[4]", "Code Agent — generating MVC code from the spec")
    code_agent = CodeAgent(llm=llm, stack=stack)
    code_dir = output_dir / "generated" / ir["project_name"]
    verification = None
    if verify:
        verifier = VerificationAgent(verify_model=verify_model, passes=verify_passes)
        generated_code, verification = _timed(
            "code_verify", stages,
            lambda: generate_and_verify(ir, code_agent, verifier, max_rounds=verify_rounds),
        )
    elif certify and stack == "python":
        from src.cleanroom.agents.verification.crosshair_verify import crosshair_available
        print("Deterministic fix loop: executable canonical I/O"
              + (" + CrossHair symbolic verification" if crosshair_available()
                 else "  (CrossHair unavailable — z3 not found, skipping symbolic step)"))
        generated_code = _timed(
            "code_exec_fix", stages,
            lambda: generate_and_verify(ir, code_agent, max_rounds=2)[0],
        )
    else:
        generated_code = _timed("code", stages, lambda: code_agent.generate(ir))
    ir = {**ir, "generated_code": generated_code.model_dump()}
    metrics["code"] = code_stats(ir["generated_code"])
    stat = metrics["code"]
    if stack == "fastapi":
        app_dir = build_runnable_package(ir["generated_code"], code_dir)
        metrics["code"]["runnable_app"] = str(app_dir)
        print(f"{stat['files']} file(s); {stat['lines_of_code']} LOC ({stat['language']}); "
              f"layers={stat['files_per_layer']}")
        print(f"Assembled runnable FastAPI app: {app_dir}  (cd \"{code_dir}\" && python -m app)")
    else:
        written = CodeAgent.write_files(generated_code, code_dir)
        print(f"Wrote {len(written)} file(s); {stat['lines_of_code']} LOC "
              f"({stat['language']}); layers={stat['files_per_layer']}")

    if verification is not None:
        ir = {**ir, "verification": verification.model_dump()}
        metrics["verification"] = {
            "max_rounds": verification.max_rounds,
            "rounds_used": verification.rounds_used,
            "n_passing": verification.n_passing,
            "n_failing": verification.n_failing,
            "residual_failures": verification.residual_failures,
        }
        report_path = VerificationAgent.write_report(verification, code_dir)
        print(f"Verification: {verification.n_passing}/{verification.n_contracts} contracts pass "
              f"({verification.rounds_used}/{verification.max_rounds} revise rounds)")
        if verification.residual_failures:
            print(f"  Residual failures: {', '.join(verification.residual_failures)}")
        print(f"  Report: {report_path}")

    # --- Stage 5: Test (LLM) -------------------------------------------------
    # The Test Agent reads only ir['features']; the generated_code in the IR is
    # structurally ignored — isolation is preserved.
    _banner("[5]", "Test Agent — deriving black-box tests from the spec")
    generated_tests = _timed("test", stages, lambda: TestAgent(llm=llm, stack=stack).generate(ir))
    ir = {**ir, "generated_tests": generated_tests.model_dump()}
    tests_dir = output_dir / "generated" / ir["project_name"] / "tests"
    written_tests = TestAgent.write_files(generated_tests, tests_dir)
    total_cases = sum(len(f.cases) for f in generated_tests.features)
    metrics["tests"] = {"features": len(generated_tests.features), "cases": total_cases}
    print(f"{len(generated_tests.features)} feature(s), {total_cases} test case(s).")
    print(f"Wrote {len(written_tests)} pytest module(s) (test_feature_*.py) to {tests_dir}")

    # --- Stage 6: Certification (optional) -------------------------------------
    if certify:
        verify_note = " (samples verified)" if verify else ""
        _banner("[6]", f"Certification Agent — pass@k (n={samples} samples){verify_note}")
        cert = _timed(
            "certification",
            stages,
            lambda: CertificationAgent(
                code_llm=llm,
                n=samples,
                stack=stack,
                verify=verify,
                verify_rounds=verify_rounds,
                verify_model=verify_model,
                verify_passes=verify_passes,
            ).run(ir),
        )
        ir = {**ir, "certification": cert.model_dump()}
        metrics["certification"] = {
            "n": cert.n,
            "k_values": cert.k_values,
            "aggregate_pass_at": cert.aggregate_pass_at,
            "aggregate_case_pass_rate": cert.aggregate_case_pass_rate,
        }
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
    if metrics.get("verification"):
        v = metrics["verification"]
        lines += [
            "",
            "## Verification (contract conformance)",
            "",
            f"- max rounds: {v['max_rounds']}",
            f"- rounds used: {v['rounds_used']}",
            f"- passing: {v['n_passing']}",
            f"- failing: {v['n_failing']}",
        ]
        if v.get("residual_failures"):
            lines += [f"- residual failures: {', '.join(v['residual_failures'])}"]
    if metrics.get("certification"):
        cert = metrics["certification"]
        lines += ["", "## Certification (pass@k)", "", f"- samples n={cert['n']}"]
        lines += [f"- {k}: {v:.3f}" for k, v in cert["aggregate_pass_at"].items()]
        if "aggregate_case_pass_rate" in cert:
            lines.append(f"- case pass rate: {cert['aggregate_case_pass_rate']:.3f}")
    if metrics.get("dafny"):
        d = metrics["dafny"]
        lines += [
            "",
            "## Dafny verification (LemmaFit)",
            "",
            f"- model: {d.get('model', 'n/a')}",
            f"- features: {d['n_features']} · verified: {d['n_verified']} · rate: {d['verification_rate']:.3f}",
        ]
        for f in d["features"]:
            mark = "verified" if f["verified"] else "UNVERIFIED"
            lines.append(f"  - {f['feature_id']} ({f['module']}): {mark} ({f['rounds']}r)")
    if metrics.get("compile"):
        c = metrics["compile"]
        lines += [
            "",
            "## TypeScript compile (dafny2js)",
            "",
            f"- compiled: {len(c.get('compiled', []))} · failed: {len(c.get('failed', []))}",
        ]
    dest.write_text("\n".join(lines) + "\n")


def _persist_run_artifacts(
    metrics: dict,
    *,
    status: str,
    output_dir: Path,
    srs_stem: str,
) -> dict:
    """Write per-run record, update RUN_RESULTS.md and API_USAGE.md."""
    run_id = make_run_id(metrics.get("srs") or srs_stem)
    metrics["run_id"] = run_id
    runs_dir = output_dir / "runs"
    recorded = record_run(metrics, status=status, runs_dir=runs_dir)
    usage_log = append_usage_log(
        metrics,
        status=status,
        run_id=run_id,
        result_path=recorded["markdown"],
    )
    recorded["usage_log"] = usage_log
    return recorded


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full Agentic Cleanroom pipeline on an SRS document.")
    parser.add_argument("srs_path", type=Path, help="Path to the SRS XML document")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Where to write artifacts")
    parser.add_argument("--certify", action="store_true", help="Also run the pass@k certification stage.")
    parser.add_argument("--samples", type=int, default=3, help="Code samples per FR for pass@k (default: 3).")
    parser.add_argument("--stack", default="auto",
                        help="Target stack: 'auto' (default, from the SRS), 'python', 'fastapi', or "
                             "'lemmafit' (verified Dafny → TypeScript; needs the lemmafit CLI + gpt-4.1).")
    parser.add_argument("--verify", action="store_true",
                        help="Run the independent verification agent after code generation (spec-level review + bounded revise loop).")
    parser.add_argument("--verify-rounds", type=int, default=2,
                        help="Max verify->revise rounds per contract (default: 2). Use 0 for one generate + one verify, no revise.")
    parser.add_argument("--verify-model", default="gpt-4o-mini",
                        help="Model for the verification agent (default: gpt-4o-mini).")
    parser.add_argument("--verify-passes", type=int, default=1,
                        help="Independent reviewer passes per contract; >1 requires unanimous fail (default: 1).")
    args = parser.parse_args()

    if not args.srs_path.exists():
        parser.error(f"SRS file not found: {args.srs_path}")

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY is not set. Add it to your .env file.")
        sys.exit(1)

    metrics: dict | None = None
    run_config = {
        "certify": args.certify,
        "samples": args.samples,
        "verify": args.verify,
        "verify_rounds": args.verify_rounds,
        "verify_model": args.verify_model,
        "verify_passes": args.verify_passes,
    }
    try:
        ir, metrics = run(
            args.srs_path, args.output_dir,
            certify=args.certify, samples=args.samples, stack=args.stack,
            verify=args.verify, verify_rounds=args.verify_rounds,
            verify_model=args.verify_model, verify_passes=args.verify_passes,
        )
        ir = {**ir, "metrics": metrics}
        normalize_ir(ir)

        dest = args.output_dir / f"{args.srs_path.stem}_full_ir.json"
        dest.write_text(json.dumps(ir, indent=2))
        report = args.output_dir / f"{args.srs_path.stem}_run_report.md"
        write_run_report(metrics, report)

        recorded = _persist_run_artifacts(
            metrics,
            status="complete",
            output_dir=args.output_dir,
            srs_stem=args.srs_path.stem,
        )
        _banner("DONE", "Run complete")
        print(f"IR        : {dest}")
        print(f"Report    : {report}")
        print(f"Run record: {recorded['markdown']}")
        print(f"Run JSON  : {recorded['json']}")
        print(f"Run index : {recorded['index']}")
        print(f"Usage log : {recorded['usage_log']}")
        per_stage = "   ".join(f"{s['name']}={s['seconds']:.1f}s" for s in metrics["stages"] if s["seconds"] >= 0.01)
        print(f"Per stage : {per_stage}")
        print(f"Time      : {metrics['total_seconds']:.2f}s   Tokens: {metrics['tokens']['total']:,}   Cost: ${metrics['cost_usd']:.4f}")
    except Exception:
        partial = (
            metrics
            if metrics is not None
            else metrics_from_globals(
                srs=args.srs_path.name,
                stack=args.stack,
                stages=[],
                config=run_config,
            )
        )
        if metrics is not None:
            _finalize_metrics(partial, partial.get("stages", []))
        recorded = _persist_run_artifacts(
            partial,
            status="failed",
            output_dir=args.output_dir,
            srs_stem=args.srs_path.stem,
        )
        print(f"Run record: {recorded['markdown']}  (partial)")
        print(f"Usage log : {recorded['usage_log']}  (partial tokens recorded)")
        raise


if __name__ == "__main__":
    main()
