#!/usr/bin/env python3
"""Side-by-side A/B: baseline-prompt DeepSeek vs CoT-prompt DeepSeek (same pipeline).

Baseline rows come from experiment_metrics.csv (deepseek rows); CoT rows come from
cot_deepseek_results.csv. Keyed by (srs, language). Emits cot_vs_baseline_deepseek.csv with
baseline_X / cot_X / delta_X for each metric, so the prompting-technique effect is one glance.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE_CSV = ROOT / "experiment_metrics.csv"
COT_CSV = ROOT / "cot_deepseek_results.csv"
OUT = ROOT / "cot_vs_baseline_deepseek.csv"

# metric -> (baseline column name, cot column name)
METRICS = {
    "verification_pass_ratio": ("verification_pass_ratio", "verification_pass_ratio"),
    "test_case_pass_ratio": ("test_case_pass_ratio", "test_case_pass_ratio"),
    "avg_input_token": ("avg_input_token", "avg_input_token"),
    "avg_output_token": ("avg_output_token", "avg_output_token"),
    "total_time": ("total_time", "total_time"),
    "avg_verification_iter": ("avg_verification_iter", "avg_verification_iter"),
    "avg_test_iter": ("avg_test_iter", "avg_test_iter"),
    "PassVer@1": ("PassVer@1", "PassVer@1"),
    "total_tokens": ("tokens_total", "total_tokens"),
}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _load(path: Path, deepseek_only: bool) -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    if not path.exists():
        return out
    with path.open() as f:
        for r in csv.DictReader(f):
            if deepseek_only and "deepseek" not in (r.get("model", "").lower()):
                continue
            out[(r.get("srs", ""), r.get("language", ""))] = r
    return out


def main() -> None:
    base = _load(BASELINE_CSV, deepseek_only=True)
    cot = _load(COT_CSV, deepseek_only=False)

    cols = ["srs", "language"]
    for m in METRICS:
        cols += [f"baseline_{m}", f"cot_{m}", f"delta_{m}"]

    keys = sorted(set(base) | set(cot))
    rows = []
    for srs, lang in keys:
        b, c = base.get((srs, lang), {}), cot.get((srs, lang), {})
        row = {"srs": srs, "language": lang}
        for m, (bcol, ccol) in METRICS.items():
            bv, cv = b.get(bcol, ""), c.get(ccol, "")
            row[f"baseline_{m}"] = bv
            row[f"cot_{m}"] = cv
            nb, nc = _num(bv), _num(cv)
            row[f"delta_{m}"] = round(nc - nb, 4) if (nb is not None and nc is not None) else ""
        rows.append(row)

    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.name}  ({len(rows)} (srs,language) pairs)")


if __name__ == "__main__":
    main()
