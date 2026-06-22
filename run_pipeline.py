"""End-to-end Agentic Cleanroom pipeline.

Runs the full pipeline on a single SRS document and saves the enriched IR:

    SRS.xml
      -> [1] Spec        FR parse + behavioral contracts    [parse: deterministic, contracts: LLM]
      -> [2] Dependency  nested graph (feature + FR level)  [regex deterministic, inner: LLM semantic]
      -> [3] Planning    impl metadata per FR contract      [LLM: signature/layer; docstring deterministic]
      -> [4a] Proof tier   prove feature logic in Dafny     [Dafny verifier + gpt-4.1, opt-in via --prove]
      -> [4] Code        adapters over proved cores + full code for the rest  [LLM: one call per contract]
      -> [4b] Verification  contract conformance + revise   [LLM, opt-in via --verify]
      -> [5] Test        black-box test cases               [LLM: one call per feature]
      -> [6] Certification  pass@k for UN-proved features   [executable oracle, opt-in via --certify]

Per-feature guarantee (FastAPI + --prove): a feature PROVED in [4a] ships its LOGIC as the compiled
Dafny core, and the Code Agent writes only a thin adapter over it (Stage 4); everything else gets
full code certified by pass@k in [6] (prove-or-test fallback). The proof tier runs BEFORE codegen
so the Code Agent knows which features ship from Dafny.

Requires OPENAI_API_KEY in .env. The proof tier additionally needs a `dafny` binary on PATH/$DAFNY.

Usage:
    uv run python run_pipeline.py "data/srs/dineout_srs.xml"
    uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --samples 1
    uv run python run_pipeline.py "data/srs/dineout_srs.xml" --prove --certify --samples 3
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
from src.cleanroom.utils.cost import estimate_cost, estimate_cost_by_model
from src.cleanroom.utils.llm_client import get_llm
from src.cleanroom.utils.dafny_project import compile_dafny, scaffold_dafny_project, stage_dafny_cores
from src.cleanroom.utils.packager import build_runnable_package
from src.cleanroom.utils.stack_select import select_stack
from src.cleanroom.utils.ir import normalize_ir
from src.cleanroom.utils.run_record import make_run_id, record_run
from src.cleanroom.utils.usage_log import append_usage_log, metrics_from_globals

# The Dafny proof tier needs a strong model — the spikes showed gpt-4o-mini/gpt-4o cannot
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
    cost, by_model = estimate_cost_by_model(GLOBAL_METRICS.calls)
    # Accurate per-model cost (a --prove run mixes gpt-4o-mini + gpt-4.1); show all models used.
    metrics["model"] = "+".join(sorted(by_model)) if len(by_model) > 1 else (GLOBAL_METRICS.model or "gpt-4o-mini")
    metrics["total_seconds"] = round(sum(s["seconds"] for s in stages), 3)
    metrics["tokens"] = {"input": in_tot, "output": out_tot, "total": in_tot + out_tot, "calls": calls}
    metrics["cost_usd"] = cost
    metrics["cost_by_model"] = by_model


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
    prove: bool = False,
    prove_target: str = "py",
) -> tuple[dict, dict]:
    stages: list = []
    run_config = {
        "certify": certify,
        "samples": samples,
        "verify": verify,
        "verify_rounds": verify_rounds,
        "verify_model": verify_model,
        "verify_passes": verify_passes,
        "prove": prove,
        "prove_target": prove_target,
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

    # --- Stage 4a: Proof tier (Dafny) — prove each feature's logic where possible -----
    # Runs BEFORE code generation so the Code Agent knows which features ship from Dafny. A PROVED
    # feature's logic ships as the compiled Dafny core (the Code Agent writes only a thin adapter
    # over it); everything else gets full code + pass@k. Degrades gracefully: no --prove or no dafny
    # binary => 0 proved => normal codegen for all features.
    proved_feature_ids: set[str] = set()
    proved_modules: dict[str, str] = {}        # feature_id -> Dafny module base (e.g. "F4_1")
    proved_sources: dict[str, str] = {}        # feature_id -> Dafny source
    proj = None
    if prove:
        _banner("[4a]", "Dafny Proof Agent — proving feature logic (formal verification)")
        from src.cleanroom.utils.dafny_verify import dafny_available
        if not dafny_available():
            print("  dafny binary not found — skipping proof tier (every feature falls to code+test).")
        else:
            project_dir = output_dir / "generated" / ir["project_name"] / "dafny_proof"
            proj = _timed("scaffold", stages, lambda: scaffold_dafny_project(project_dir))
            gen = _timed("dafny", stages, lambda: DafnyAgent(proj, model=_DAFNY_MODEL).generate(ir))
            (proj / "SPEC.yaml").write_text(gen.spec_yaml)
            proved_feature_ids = {f.feature_id for f in gen.features if f.verified}
            proved_modules = {f.feature_id: f.module for f in gen.features if f.verified}
            proved_sources = {f.feature_id: f.dafny_source for f in gen.features if f.verified}
            ntot, nver = len(gen.features), gen.n_verified
            n_axiom = sum(1 for f in gen.features if f.verified and f.axioms)
            ax_note = f"  ({n_axiom} via assumed axioms)" if n_axiom else ""
            print(f"Proved    : {nver}/{ntot} features{ax_note}  →  {sorted(proved_feature_ids) or '(none)'}")
            for f in gen.features:
                label = "PROVED " if f.verified else "unproved"
                axt = f"  [{len(f.axioms)} assumed axiom(s)]" if f.verified and f.axioms else ""
                print(f"  [{f.feature_id}] {label}  {f.module}  ({f.rounds}r){axt}")
            metrics["dafny"] = {
                "model": _DAFNY_MODEL, "n_features": ntot, "n_verified": nver,
                "n_proved_with_axioms": n_axiom,
                "verification_rate": round(nver / ntot, 3) if ntot else 0.0,
                "features": [{"feature_id": f.feature_id, "module": f.module,
                              "verified": f.verified, "rounds": f.rounds,
                              "axioms": len(f.axioms)} for f in gen.features],
            }
            comp = _timed("compile", stages, lambda: compile_dafny(proj, gen, target=prove_target))
            metrics["compile"] = comp
            print(f"Compiled  : {len(comp['compiled'])}/{nver} proved features to {comp.get('target', prove_target)}")
            ir = {**ir, "generated_dafny": gen.model_dump(),
                  "proved_feature_ids": sorted(proved_feature_ids)}

    # Adapter shipping (Dafny core + thin glue) is the FastAPI design; proved features there ship
    # from Dafny and are excluded from pass@k. On the python stack --prove is proof-only (extra
    # certification) and code/test proceed normally for every feature.
    adapter_mode = bool(proved_feature_ids) and stack == "fastapi"
    cert_skip = set(proved_feature_ids) if adapter_mode else set()

    # --- Stage 4: Code (LLM) — adapters over proved cores + full code for the rest ----
    _banner("[4]", "Code Agent — generating MVC code from the spec")
    code_agent = CodeAgent(llm=llm, stack=stack)
    code_dir = output_dir / "generated" / ir["project_name"]
    verification = None
    if adapter_mode:
        from src.cleanroom.agents.code.schema.code import GeneratedCode
        adapters = []
        for fid in sorted(proved_feature_ids):
            adapters.append(_timed(
                "adapter", stages,
                lambda fid=fid: code_agent.generate_adapter(
                    ir, fid, proved_modules[fid], proved_sources[fid])))
        full = _timed("code", stages,
                      lambda: code_agent.generate(ir, skip_feature_ids=proved_feature_ids))
        generated_code = GeneratedCode(files=adapters + full.files)
        print(f"  {len(adapters)} proved feature(s) shipped as Dafny-core adapters; "
              f"{len(full.files)} file(s) generated for the rest.")
    elif verify:
        verifier = VerificationAgent(verify_model=verify_model, passes=verify_passes)
        generated_code, verification = _timed(
            "code_verify", stages,
            lambda: generate_and_verify(ir, code_agent, verifier, max_rounds=verify_rounds),
        )
    else:
        generated_code = _timed("code", stages, lambda: code_agent.generate(ir))
    ir = {**ir, "generated_code": generated_code.model_dump()}
    metrics["code"] = code_stats(ir["generated_code"])
    stat = metrics["code"]
    if stack == "fastapi":
        app_dir = build_runnable_package(ir["generated_code"], code_dir)
        metrics["code"]["runnable_app"] = str(app_dir)
        if adapter_mode and proj is not None:
            staged = stage_dafny_cores(Path(app_dir), proj,
                                       [proved_modules[fid] for fid in sorted(proved_feature_ids)])
            metrics["code"]["dafny_cores"] = staged
            print(f"  Staged proved Dafny cores {staged['staged']} + shim into {staged['cores_dir']}")
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

    # --- Stage 6: Certification (optional) — pass@k for the UN-proved (test fallback) --
    if certify:
        verify_note = " (samples verified)" if verify else ""
        skip_note = f" · skipping {len(cert_skip)} proved" if cert_skip else ""
        _banner("[6]", f"Certification Agent — pass@k (n={samples} samples){verify_note}{skip_note}")
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
                skip_feature_ids=cert_skip,
                dafny_proj=proj if adapter_mode else None,
                dafny_modules=[proved_modules[fid] for fid in sorted(proved_feature_ids)] if adapter_mode else None,
            ).run(ir),
        )
        ir = {**ir, "certification": cert.model_dump()}
        metrics["certification"] = {
            "n": cert.n,
            "k_values": cert.k_values,
            "aggregate_pass_at": cert.aggregate_pass_at,
            "aggregate_case_pass_rate": cert.aggregate_case_pass_rate,
            "n_tested_frs": len(cert.frs),
            "n_proved_features": len(proved_feature_ids),
        }
        if not cert.frs:
            print("  (no features to test — all were certified by the proof tier)")
        else:
            for k, v in cert.aggregate_pass_at.items():
                print(f"  {k}: {v:.3f}  (over {len(cert.frs)} un-proved FR(s))")

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
    by_model = metrics.get("cost_by_model") or {}
    if len(by_model) > 1:
        lines.append("- per-model (accurate mixed-model cost):")
        for m, agg in sorted(by_model.items()):
            lines.append(f"  - {m}: {agg['calls']} call(s), "
                         f"{agg['input'] + agg['output']:,} tok, ${agg['cost_usd']:.4f}")
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
            "## Dafny proof tier (formal verification)",
            "",
            f"- model: {d.get('model', 'n/a')}",
            f"- features: {d['n_features']} · proved: {d['n_verified']} · rate: {d['verification_rate']:.3f}",
        ]
        if d.get("n_proved_with_axioms"):
            lines.append(f"- of which {d['n_proved_with_axioms']} rely on assumed axioms (not fully discharged)")
        for f in d["features"]:
            mark = "PROVED" if f["verified"] else "unproved (→ test track)"
            axt = f" [{f['axioms']} assumed axiom(s)]" if f.get("axioms") else ""
            lines.append(f"  - {f['feature_id']} ({f['module']}): {mark} ({f['rounds']}r){axt}")
    if metrics.get("compile"):
        c = metrics["compile"]
        lines += [
            "",
            f"## Native compile (dafny translate {c.get('target', 'py')})",
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
    parser.add_argument("--stack", default="auto", choices=["auto", "python", "fastapi"],
                        help="MVC app stack: 'auto' (default, from the SRS), 'python', or 'fastapi'.")
    parser.add_argument("--prove", action="store_true",
                        help="Run the Dafny proof tier: prove each feature's logic where possible "
                             "(needs a `dafny` binary + gpt-4.1). Proved features compile to native "
                             "code; with --certify the rest fall to the pass@k test track.")
    parser.add_argument("--prove-target", default="py",
                        choices=["py", "cs", "js", "go", "java", "cpp", "rs"],
                        help="dafny translate target for proved features (default: py).")
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
        "prove": args.prove,
        "prove_target": args.prove_target,
    }
    try:
        ir, metrics = run(
            args.srs_path, args.output_dir,
            certify=args.certify, samples=args.samples, stack=args.stack,
            verify=args.verify, verify_rounds=args.verify_rounds,
            verify_model=args.verify_model, verify_passes=args.verify_passes,
            prove=args.prove, prove_target=args.prove_target,
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
