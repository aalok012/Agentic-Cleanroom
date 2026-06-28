#!/usr/bin/env python3
"""Rerun Java/Spring certification from saved matrix IRs.

This is intentionally narrower than ``run_pipeline.py``: it does not call spec,
dependency, planning, proof, code, or test generation. It reuses each
``*_full_ir.json`` artifact, applies a deterministic cleanup for older Dafny
Spring adapters, reruns the Maven compile oracle, updates the saved metrics, and
lets ``scripts/collect_metrics.py`` rebuild the CSV.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from run_pipeline import _compute_summary  # noqa: E402
from src.cleanroom.agents.evaluation.agent import CertificationAgent  # noqa: E402


class NoLLM:
    model_name = "saved-java-recert-no-llm"


def _module_packages(module: str) -> tuple[str, str]:
    return f"{module}Domain".replace("_", "__"), f"{module}Kernel".replace("_", "__")


def _compiled_adapter_modules(ir: dict, cell_dir: Path) -> dict[str, str]:
    """feature_id -> Dafny module for verified cores that have translated Java output."""
    project = ir.get("project_name", "project")
    dafny_proj = cell_dir / "generated" / project / "dafny_proof"
    out: dict[str, str] = {}
    for feature in (ir.get("generated_dafny") or {}).get("features", []):
        module = feature.get("module")
        fid = str(feature.get("feature_id", ""))
        if feature.get("verified") and module and (dafny_proj / "out" / f"{module}-java").is_dir():
            out[fid] = module
    return out


def _strip_invalid_package_imports(content: str, names: list[str]) -> str:
    for name in names:
        content = re.sub(rf"(?m)^\s*import\s+{re.escape(name)}\s*;\s*\n?", "", content)
    return content


def _repair_adapter_content(content: str, modules: list[str]) -> tuple[str, bool]:
    """Fix old Spring adapters that referenced Dafny's unimportable default-package facade.

    Dafny's Java backend writes useful classes into packages like ``F3__1Domain``.
    Older adapters sometimes referenced ``F3_1.Model`` / ``F3_1.__default`` instead,
    which cannot compile from a named Spring package. This rewrite is mechanical and
    does not use test results or LLM output.
    """
    before = content
    for module in modules:
        domain, kernel = _module_packages(module)
        module_domain = f"{module}Domain"
        module_kernel = f"{module}Kernel"
        content = _strip_invalid_package_imports(content, [module, domain, kernel, module_domain, module_kernel])

        # Collapse odd nested references first, then route all top-level module references
        # through the translated Domain package.
        for prefix in (module_domain, domain):
            content = content.replace(f"{module}.{prefix}.", f"{domain}.")
            content = content.replace(f"{domain}.{prefix}.", f"{domain}.")
        content = content.replace(f"{module}.{module_kernel}.", f"{kernel}.")
        content = content.replace(f"{module}.{kernel}.", f"{kernel}.")
        content = re.sub(rf"\b{re.escape(module)}\.", f"{domain}.", content)
        content = content.replace(f"{domain}.{domain}.", f"{domain}.")
        content = content.replace(f"{kernel}.{kernel}.", f"{kernel}.")

    # Dafny 4 Java runtime represents strings as CodePoint sequences.
    content = content.replace("DafnySequence<Character>", "DafnySequence<? extends dafny.CodePoint>")
    content = content.replace("DafnySequence<? extends Character>", "DafnySequence<? extends dafny.CodePoint>")
    content = content.replace("DafnySequence.asString(", "DafnySequence.asUnicodeString(")
    return content, content != before


def repair_saved_adapters(ir: dict, cell_dir: Path) -> int:
    modules_by_feature = _compiled_adapter_modules(ir, cell_dir)
    if not modules_by_feature:
        return 0
    changed = 0
    files = (ir.get("generated_code") or {}).get("files") or []
    for generated_file in files:
        fid = str(generated_file.get("feature_id", ""))
        module = modules_by_feature.get(fid)
        content = generated_file.get("content") or ""
        if not module or "Adapter" not in (generated_file.get("path") or ""):
            continue
        repaired, did_change = _repair_adapter_content(content, [module])
        if did_change:
            generated_file["content"] = repaired
            changed += 1
    return changed


def _latest_run_json(cell_dir: Path) -> Path | None:
    candidates = sorted((cell_dir / "runs").glob("*.json"))
    if not candidates:
        return None

    def key(path: Path) -> str:
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("timestamp_utc", "")
        except (json.JSONDecodeError, OSError):
            return ""

    return max(candidates, key=key)


def _update_run_record(cell_dir: Path, metrics: dict) -> bool:
    run_json = _latest_run_json(cell_dir)
    if run_json is None:
        return False
    try:
        rec = json.loads(run_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    for key in ("certification", "tests", "code", "dafny", "compile", "java_saved_adapter_repair"):
        if key in metrics:
            rec[key] = metrics[key]
    rec["status"] = "complete"
    rec["recertified_at_utc"] = metrics.get("recertified_at_utc")
    run_json.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return True


def recertify(full_ir_path: Path, timeout: float) -> dict:
    cell_dir = full_ir_path.parent
    ir = json.loads(full_ir_path.read_text(encoding="utf-8"))
    metrics = ir.setdefault("metrics", {})
    adapter_modules = _compiled_adapter_modules(ir, cell_dir)
    changed = repair_saved_adapters(ir, cell_dir)

    dafny_proj = cell_dir / "generated" / ir.get("project_name", "project") / "dafny_proof"
    cert = CertificationAgent(
        code_llm=NoLLM(),
        n=1,
        k_values=(1,),
        stack="spring",
        language="java",
        case_timeout=timeout,
        skip_feature_ids=set(adapter_modules),
        dafny_proj=dafny_proj if adapter_modules else None,
        dafny_modules=[adapter_modules[fid] for fid in sorted(adapter_modules)] if adapter_modules else None,
    ).certify(ir)

    ir["certification"] = cert.model_dump()
    metrics["certification"] = {
        "n": cert.n,
        "k_values": cert.k_values,
        "aggregate_pass_at": cert.aggregate_pass_at,
        "aggregate_case_pass_rate": cert.aggregate_case_pass_rate,
        "n_tested_frs": len(cert.frs),
        "n_proved_features": len(ir.get("proved_feature_ids") or []),
        "n_total_tested_features": len(cert.features),
        "pass_at_1_fr_ids": sorted(fr.fr_id for fr in cert.frs if fr.pass_at.get("pass@1", 0.0) >= 1.0),
    }
    metrics["proved_feature_ids"] = sorted(ir.get("proved_feature_ids") or [])
    metrics["java_saved_adapter_repair"] = {
        "adapter_files_changed": changed,
        "compiled_adapter_features": sorted(adapter_modules),
    }
    metrics["recertified_at_utc"] = datetime.now(UTC).isoformat()
    metrics["summary"] = _compute_summary(metrics, ir)

    full_ir_path.write_text(json.dumps(ir, indent=2) + "\n", encoding="utf-8")
    run_record_updated = _update_run_record(cell_dir, metrics)
    return {
        "cell": str(cell_dir),
        "changed_adapters": changed,
        "run_record_updated": run_record_updated,
        "tested_frs": len(cert.frs),
        "pass@1": cert.aggregate_pass_at.get("pass@1", 0.0),
        "case_pass_rate": cert.aggregate_case_pass_rate,
        "PassVer@1": metrics["summary"].get("PassVer@1"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Recertify saved Java/Spring matrix IRs without generation.")
    parser.add_argument("--root", type=Path, default=Path("outputs/matrix/java"))
    parser.add_argument("--timeout", type=float, default=240.0)
    parser.add_argument("--cell", type=str, default="", help="Optional substring filter for one cell path.")
    parser.add_argument("--log", type=Path, default=Path("outputs/java_recert.log"))
    args = parser.parse_args()

    paths = sorted(args.root.glob("*/*/*_full_ir.json"))
    if args.cell:
        paths = [p for p in paths if args.cell in str(p.parent)]

    args.log.parent.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    skipped = 0
    with args.log.open("w", encoding="utf-8") as log:
        for path in paths:
            print(f"recertifying {path.parent}")
            try:
                with contextlib.redirect_stdout(log):
                    result = recertify(path, timeout=args.timeout)
                print(
                    f"  pass@1={result['pass@1']:.3f} "
                    f"case={result['case_pass_rate']:.3f} "
                    f"PassVer@1={result['PassVer@1']} "
                    f"changed_adapters={result['changed_adapters']}"
                )
                results.append(result)
            except Exception as exc:  # keep the batch moving, like run_matrix.sh
                skipped += 1
                print(f"  FAIL: {type(exc).__name__}: {exc}")
                print(f"\n\n### {path.parent}\n{type(exc).__name__}: {exc}", file=log)

    print(f"recertified={len(results)} failed={skipped} log={args.log}")


if __name__ == "__main__":
    main()
