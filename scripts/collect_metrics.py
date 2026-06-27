#!/usr/bin/env python3
"""Aggregate every per-run metrics JSON into one flat CSV.

Each pipeline run writes ``<output-dir>/runs/<run_id>.json`` (see
src/cleanroom/utils/run_record.py). This walks all of them under --root, flattens
each into a single row, and rebuilds --out from scratch (idempotent — safe to
re-run after every pipeline cell). One row per run, keyed/deduped by run_id.

The matrix runner (run_matrix.sh) lays runs out as
``outputs/<language>/<srs_stem>/<model_safe>/runs/<run_id>.json``; language / srs /
model are derived from that path when possible, falling back to the JSON body so
older flat layouts still aggregate.

Usage:
    uv run python scripts/collect_metrics.py [--root outputs] [--out experiment_metrics.csv]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

COLUMNS = [
    "run_id", "timestamp", "status", "language", "srs", "stack", "model",
    "total_seconds",
    "tokens_in", "tokens_out", "tokens_total", "llm_calls", "cost_usd",
    "code_files", "code_loc", "test_features", "test_cases",
    "dafny_n_features", "dafny_n_verified", "dafny_verification_rate", "dafny_axioms",
    "cert_n", "pass@1", "case_pass_rate", "n_tested_frs", "n_proved_features",
    "prove", "certify", "samples", "max_cert_loops", "temperature",
]


def _derive_from_path(json_path: Path, root: Path) -> dict:
    """Pull language / srs / model from outputs/<lang>/<srs>/<model>/runs/<id>.json."""
    out: dict = {}
    try:
        # parts after root: <language>/<srs_stem>/<model_safe>/runs/<file>
        rel = json_path.relative_to(root).parts
    except ValueError:
        rel = json_path.parts
    if len(rel) >= 5 and rel[-2] == "runs":
        out["language"] = rel[-5]
        out["srs"] = rel[-4]
        out["model"] = rel[-3]
    return out


def _row(rec: dict, path_hint: dict) -> dict:
    cfg = rec.get("config") or {}
    tok = rec.get("tokens") or {}
    code = rec.get("code") or {}
    tests = rec.get("tests") or {}
    dafny = rec.get("dafny") or {}
    cert = rec.get("certification") or {}
    pass_at = cert.get("aggregate_pass_at") or {}

    return {
        "run_id": rec.get("run_id", ""),
        "timestamp": rec.get("timestamp_utc", ""),
        "status": rec.get("status", ""),
        # path is authoritative for the matrix layout; JSON body is the fallback.
        "language": path_hint.get("language") or rec.get("language") or cfg.get("language", ""),
        "srs": path_hint.get("srs") or (Path(rec["srs"]).stem if rec.get("srs") else ""),
        "stack": rec.get("stack") or cfg.get("stack", ""),
        "model": path_hint.get("model") or rec.get("model", ""),
        "total_seconds": rec.get("total_seconds", ""),
        "tokens_in": tok.get("input", ""),
        "tokens_out": tok.get("output", ""),
        "tokens_total": tok.get("total", ""),
        "llm_calls": tok.get("calls", ""),
        "cost_usd": rec.get("cost_usd", ""),
        "code_files": code.get("files", ""),
        "code_loc": code.get("lines_of_code", ""),
        "test_features": tests.get("features", ""),
        "test_cases": tests.get("cases", ""),
        "dafny_n_features": dafny.get("n_features", ""),
        "dafny_n_verified": dafny.get("n_verified", ""),
        "dafny_verification_rate": dafny.get("verification_rate", ""),
        "dafny_axioms": dafny.get("n_proved_with_axioms", ""),
        "cert_n": cert.get("n", ""),
        "pass@1": pass_at.get("pass@1", ""),
        "case_pass_rate": cert.get("aggregate_case_pass_rate", ""),
        "n_tested_frs": cert.get("n_tested_frs", ""),
        "n_proved_features": cert.get("n_proved_features", ""),
        "prove": cfg.get("prove", ""),
        "certify": cfg.get("certify", ""),
        "samples": cfg.get("samples", ""),
        "max_cert_loops": cfg.get("max_cert_loops", ""),
        "temperature": cfg.get("temperature", ""),
    }


def collect(root: Path, out: Path) -> int:
    rows: dict[str, dict] = {}  # run_id -> row (dedupe; last write wins)
    for json_path in sorted(root.glob("**/runs/*.json")):
        try:
            rec = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  skip {json_path}: {e}")
            continue
        row = _row(rec, _derive_from_path(json_path, root))
        rid = row["run_id"] or json_path.stem
        rows[rid] = row

    ordered = sorted(rows.values(), key=lambda r: (r.get("timestamp") or "", r.get("run_id") or ""))
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ordered)
    return len(ordered)


def main() -> None:
    ap = argparse.ArgumentParser(description="Aggregate per-run metrics JSON into one CSV.")
    ap.add_argument("--root", type=Path, default=Path("outputs"), help="Dir to scan (default: outputs)")
    ap.add_argument("--out", type=Path, default=Path("experiment_metrics.csv"), help="CSV path (default: experiment_metrics.csv)")
    args = ap.parse_args()

    if not args.root.exists():
        print(f"root {args.root} does not exist — nothing to collect")
        return
    n = collect(args.root, args.out)
    print(f"wrote {n} run(s) -> {args.out}")


if __name__ == "__main__":
    main()
