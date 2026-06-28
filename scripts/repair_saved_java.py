#!/usr/bin/env python3
"""Run Java compile repair on saved matrix IRs, then recertify.

This is the token-consuming follow-up to ``recertify_saved_java.py``. It still
avoids a full pipeline rerun: no SRS parsing, planning, proof, code generation,
or test generation is repeated. Only generated Java files that Maven maps to
compiler errors are sent through the compile-repair prompts.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
load_dotenv()

from scripts.recertify_saved_java import (  # noqa: E402
    _compiled_adapter_modules,
    recertify,
    repair_saved_adapters,
)
from src.cleanroom.agents.code.agent import CodeAgent  # noqa: E402
from src.cleanroom.agents.code.compile_repair import run_java_compile_repair  # noqa: E402
from src.cleanroom.agents.test.agent import TestAgent  # noqa: E402
from src.cleanroom.utils.code_stats import code_stats  # noqa: E402
from src.cleanroom.utils.llm_client import DEFAULT_MODEL, get_llm  # noqa: E402


def _model_from_cell(path: Path, metrics: dict, stage: str) -> str:
    """Saved-cell repairs use the current cost-control default, not the original cell model."""
    return DEFAULT_MODEL


def _needs_repair(ir: dict) -> bool:
    cert = (ir.get("metrics") or {}).get("certification") or {}
    n_tested = int(cert.get("n_tested_frs") or 0)
    case_rate = float(cert.get("aggregate_case_pass_rate") or 0.0)
    return n_tested > 0 and case_rate < 1.0


def repair_one(full_ir_path: Path, *, max_rounds: int, timeout: float, model_override: str | None) -> dict:
    cell_dir = full_ir_path.parent
    ir = json.loads(full_ir_path.read_text(encoding="utf-8"))
    metrics = ir.setdefault("metrics", {})

    adapter_changes = repair_saved_adapters(ir, cell_dir)
    adapter_modules = _compiled_adapter_modules(ir, cell_dir)
    project = ir.get("project_name", "project")
    code_dir = cell_dir / "generated" / project
    dafny_proj = code_dir / "dafny_proof"
    generated_tests = ir.get("generated_tests") or {}

    code_model = model_override or _model_from_cell(full_ir_path, metrics, "code")
    test_model = model_override or _model_from_cell(full_ir_path, metrics, "test")
    code_agent = CodeAgent(llm=get_llm(model=code_model, temperature=0.0), stack="spring", language="java")
    test_agent = TestAgent(llm=get_llm(model=test_model, temperature=0.0), stack="spring", language="java")

    repair = run_java_compile_repair(
        code_agent=code_agent,
        ir=ir,
        code_dir=code_dir,
        stack="spring",
        generated_tests=generated_tests,
        test_agent=test_agent,
        dafny_proj=dafny_proj if adapter_modules else None,
        adapter_modules=adapter_modules,
        max_rounds=max_rounds,
        timeout=timeout,
    )
    metrics["java_compile_repair"] = repair
    metrics["java_saved_adapter_repair"] = {
        "adapter_files_changed": adapter_changes,
        "compiled_adapter_features": sorted(adapter_modules),
    }

    prev_code = metrics.get("code") or {}
    next_code = code_stats(ir["generated_code"])
    next_code["language"] = "Java"
    if prev_code.get("runnable_app"):
        next_code["runnable_app"] = prev_code["runnable_app"]
    if prev_code.get("dafny_cores"):
        next_code["dafny_cores"] = prev_code["dafny_cores"]
    metrics["code"] = next_code

    full_ir_path.write_text(json.dumps(ir, indent=2) + "\n", encoding="utf-8")
    recert = recertify(full_ir_path, timeout=timeout)
    return {
        **recert,
        "repair_ok": repair.get("ok"),
        "repair_reason": repair.get("reason"),
        "repair_attempts": len(repair.get("attempts") or []),
        "repaired_files": len(repair.get("repaired_files") or []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile-repair saved Java/Spring matrix IRs.")
    parser.add_argument("--root", type=Path, default=Path("outputs/matrix/java"))
    parser.add_argument("--cell", default="", help="Optional substring filter for one or more cell paths.")
    parser.add_argument("--max-rounds", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=240.0)
    parser.add_argument("--model", default="", help="Optional override model for repair prompts; defaults to DeepSeek.")
    parser.add_argument("--all", action="store_true", help="Repair all matching full IRs, not only failing cells.")
    parser.add_argument("--log", type=Path, default=Path("outputs/java_compile_repair.log"))
    args = parser.parse_args()

    paths = sorted(args.root.glob("*/*/*_full_ir.json"))
    if args.cell:
        paths = [p for p in paths if args.cell in str(p.parent)]
    if not args.all:
        filtered: list[Path] = []
        for path in paths:
            try:
                if _needs_repair(json.loads(path.read_text(encoding="utf-8"))):
                    filtered.append(path)
            except (json.JSONDecodeError, OSError):
                pass
        paths = filtered

    args.log.parent.mkdir(parents=True, exist_ok=True)
    done = 0
    failed = 0
    with args.log.open("a", encoding="utf-8") as log:
        for path in paths:
            print(f"repairing {path.parent}")
            try:
                with contextlib.redirect_stdout(log):
                    result = repair_one(
                        path,
                        max_rounds=args.max_rounds,
                        timeout=args.timeout,
                        model_override=args.model or None,
                    )
                done += 1
                print(
                    f"  repair_ok={result['repair_ok']} repaired_files={result['repaired_files']} "
                    f"attempts={result['repair_attempts']} pass@1={result['pass@1']:.3f} "
                    f"case={result['case_pass_rate']:.3f} PassVer@1={result['PassVer@1']}"
                )
            except Exception as exc:
                failed += 1
                print(f"  FAIL: {type(exc).__name__}: {exc}")
                print(f"\n\n### {path.parent}\n{type(exc).__name__}: {exc}", file=log)
    print(f"repaired={done} failed={failed} log={args.log}")


if __name__ == "__main__":
    main()
