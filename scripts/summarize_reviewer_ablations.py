#!/usr/bin/env python3
"""Summarize completed reviewer-ablation runs without inventing missing results.

One CSV row per executed run (arm × subject × language), plus a reference
noise band (mean and standard deviation over the repeats) per subject.

Columns cover three scoring lenses from the README:
  1. own labels — per-FR label distribution + VPR / TPR / PassVer@1 (with denominators);
  2. validated oracle — label precision and (for test_sees_code) self-grading inflation;
Missing runs are marked `missing`; nothing is fabricated.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


FIELDS = [
    "subject", "model", "language", "arm", "rep", "status",
    # own-label counts (denominators are explicit)
    "n_frs", "proved_frs", "proved_with_axioms_frs", "tested_pass_frs",
    "uncertified_frs", "residual_test_denominator", "tested_frs",
    "vpr_numerator", "vpr_denominator", "passver_numerator", "passver_denominator",
    "test_pass_numerator", "test_pass_denominator", "test_case_passed", "test_case_total",
    # headline ratios
    "verification_pass_ratio", "test_case_pass_ratio", "PassVer@1", "PassVer@1_sd",
    # oracle lens (python; blank when no oracle run)
    "oracle_tested_frs", "oracle_pass_frs", "label_precision", "self_grading_inflation",
    # cost (incremental: reused stages excluded)
    "reused_stages", "input_tokens", "output_tokens", "total_tokens", "llm_calls",
    "cost_usd", "total_time", "avg_verification_iteration", "avg_test_iteration",
    "recovery_loops", "repaired_by_proof", "repaired_by_tests", "reference_repeats",
]

FR_FIELDS = ["subject", "model", "language", "arm", "rep", "feature_id", "fr_id",
             "label", "proved", "proved_with_axioms", "passes_independent_tests",
             "passver_at_1", "source_ir"]
STAGE_FIELDS = ["subject", "model", "language", "arm", "rep", "stage",
                "seconds", "input_tokens", "output_tokens", "llm_calls", "reused"]
RECOVERY_FIELDS = ["subject", "model", "language", "arm", "rep", "loop",
                   "targeted_features", "reproved_features", "still_failing_features",
                   "proved_frs", "certified_frs", "residual_frs", "total_frs",
                   "passver_numerator", "passver_denominator", "PassVer@1",
                   "pass_at_1", "case_pass_rate"]


def _fr_universe(ir: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for f in ir.get("features", []):
        out[str(f.get("id"))] = [str(r.get("id")) for r in f.get("functional_requirements", [])]
    return out


def _labels(ir: dict, metrics: dict) -> dict:
    """Per-FR label counts over the full FR universe, from saved artifacts only."""
    fr_by_feat = _fr_universe(ir)
    all_fr = {fr for ids in fr_by_feat.values() for fr in ids}
    proved_feats = set(metrics.get("proved_feature_ids") or ir.get("proved_feature_ids") or [])
    proved_fr = {fr for fid in proved_feats for fr in fr_by_feat.get(fid, [])}
    # proved-with-axioms at the feature level → its FRs
    daf = {f["feature_id"]: f for f in (metrics.get("dafny") or {}).get("features", [])}
    axiom_fr = {fr for fid in proved_feats if daf.get(fid, {}).get("axioms")
                for fr in fr_by_feat.get(fid, [])}
    cert = metrics.get("certification") or {}
    pass1_fr = set(cert.get("pass_at_1_fr_ids") or [])
    tested_pass = pass1_fr - proved_fr
    certified = proved_fr | pass1_fr
    uncertified = all_fr - certified
    return {
        "n_frs": len(all_fr),
        "proved_frs": len(proved_fr - axiom_fr),
        "proved_with_axioms_frs": len(axiom_fr),
        "tested_pass_frs": len(tested_pass),
        "uncertified_frs": len(uncertified),
        "residual_test_denominator": len(all_fr - proved_fr),
        "tested_frs": cert.get("n_tested_frs", ""),
        "vpr_numerator": len(proved_fr),
        "vpr_denominator": len(all_fr),
        "passver_numerator": len(certified),
        "passver_denominator": len(all_fr),
    }


def _oracle(ir: dict, metrics: dict) -> dict:
    """Label precision against the human-validated oracle, and self-grading inflation."""
    o = metrics.get("oracle_certification")
    if not o:
        return {}
    oracle_pass = set(o.get("pass_at_1_fr_ids") or [])
    tested = set(o.get("tested_fr_ids") or [])
    # certified-by-the-arm FRs that the independent oracle also passes / all certified (that the
    # oracle covers) = precision of the arm's "certified" claim against an outside judgment.
    cert = metrics.get("certification") or {}
    fr_by_feat = _fr_universe(ir)
    proved_feats = set(metrics.get("proved_feature_ids") or ir.get("proved_feature_ids") or [])
    certified = {fr for fid in proved_feats for fr in fr_by_feat.get(fid, [])} | set(
        cert.get("pass_at_1_fr_ids") or [])
    checkable = certified & tested
    precision = round(len(checkable & oracle_pass) / len(checkable), 4) if checkable else ""
    # self-grading inflation: own pass rate − oracle pass rate over the SAME FRs the oracle covers.
    own_pass = set(cert.get("pass_at_1_fr_ids") or []) & tested
    inflation = (round(len(own_pass) / len(tested) - len(oracle_pass) / len(tested), 4)
                 if tested else "")
    return {"oracle_tested_frs": len(tested), "oracle_pass_frs": len(oracle_pass),
            "label_precision": precision, "self_grading_inflation": inflation}


def summarize(run: dict) -> dict:
    row = {k: run.get(k, "") for k in ("subject", "language", "arm", "rep")}
    row["model"] = run.get("model", "")
    row["reused_stages"] = ",".join(run.get("reuse") or []) or "-"
    path = Path(run["output_dir"]) / (run["stem"] + "_full_ir.json")
    if not path.exists():
        return {**row, "status": "failed" if run.get("exit_code") else "missing"}
    try:
        ir = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {**row, "status": "invalid_json"}
    metrics = ir.get("metrics") or {}
    summary = metrics.get("summary") or {}
    row["model"] = (metrics.get("config") or {}).get("models", {}).get("code", "")
    lab = _labels(ir, metrics)
    row.update(lab)
    cert = metrics.get("certification") or {}
    cert_frs = (ir.get("certification") or {}).get("frs") or []
    row.update({"test_pass_numerator": len(set(cert.get("pass_at_1_fr_ids") or [])),
                "test_pass_denominator": cert.get("n_tested_frs", ""),
                "test_case_passed": sum(fr.get("cases_passed", 0) for fr in cert_frs),
                "test_case_total": sum(fr.get("cases_total", 0) for fr in cert_frs)})
    row["verification_pass_ratio"] = (round(lab["vpr_numerator"] / lab["vpr_denominator"], 4)
                                       if lab["vpr_denominator"] else 0.0)
    row["test_case_pass_ratio"] = (summary.get("test_case_pass_ratio", "")
                                    if metrics.get("certification") else "")
    row["PassVer@1"] = (round(lab["passver_numerator"] / lab["passver_denominator"], 4)
                        if lab["passver_denominator"] else 0.0)
    for key in ("PassVer@1", "verification_pass_ratio"):
        if summary.get(key) is not None and abs(float(summary[key]) - row[key]) > 0.00011:
            raise ValueError(f"{path}: computed {key} disagrees with pipeline summary")
    row.update(_oracle(ir, metrics))
    tok = metrics.get("tokens") or {}
    row.update({"input_tokens": tok.get("input", ""), "output_tokens": tok.get("output", ""),
                "total_tokens": tok.get("total", ""), "llm_calls": tok.get("calls", ""),
                "cost_usd": metrics.get("cost_usd", ""),
                "avg_verification_iteration": summary.get("avg_verification_iteration", ""),
                "avg_test_iteration": summary.get("avg_test_iteration", "")})
    rec = metrics.get("recovery") or {}
    row.update({"recovery_loops": rec.get("loops_run", 0),
                "repaired_by_proof": len(rec.get("repaired_by_proof") or []),
                "repaired_by_tests": len(rec.get("repaired_by_tests") or [])})
    row["total_time"] = summary.get("total_time", "")
    row["status"] = "complete"
    return {**{k: "" for k in FIELDS}, **row}


def detail_rows(run: dict):
    path = Path(run["output_dir"]) / (run["stem"] + "_full_ir.json")
    if not path.exists():
        return [], [], []
    ir = json.loads(path.read_text())
    metrics = ir.get("metrics") or {}
    model = (metrics.get("config") or {}).get("models", {}).get("code", "")
    base = {"subject": run["subject"], "model": model, "language": run["language"],
            "arm": run["arm"], "rep": run.get("rep") or ""}
    proved_features = set(metrics.get("proved_feature_ids") or [])
    proof_features = {str(f.get("feature_id")): f for f in (metrics.get("dafny") or {}).get("features", [])}
    pass1 = set((metrics.get("certification") or {}).get("pass_at_1_fr_ids") or [])
    fr_rows = []
    for feature in ir.get("features", []):
        fid = str(feature.get("id"))
        proved = fid in proved_features
        axioms = bool(proved and proof_features.get(fid, {}).get("axioms"))
        for req in feature.get("functional_requirements", []):
            rid = str(req.get("id"))
            tested = rid in pass1
            label = ("PROVED_WITH_AXIOMS" if axioms else "PROVED") if proved else (
                "TESTED_PASS" if tested else "UNCERTIFIED")
            fr_rows.append({**base, "feature_id": fid, "fr_id": rid, "label": label,
                            "proved": int(proved), "proved_with_axioms": int(axioms),
                            "passes_independent_tests": int(tested), "passver_at_1": int(proved or tested),
                            "source_ir": str(path)})
    stages = [{**base, "stage": s.get("name", ""), "seconds": s.get("seconds", ""),
               "input_tokens": s.get("input_tokens", ""), "output_tokens": s.get("output_tokens", ""),
               "llm_calls": s.get("calls", ""), "reused": 0}
              for s in metrics.get("stages", [])]
    stages.extend({**base, "stage": stage, "seconds": "", "input_tokens": "",
                   "output_tokens": "", "llm_calls": "", "reused": 1}
                  for stage in (metrics.get("reused") or {}).get("stages", []))
    recovery = []
    for lp in (metrics.get("recovery") or {}).get("loops", []):
        total = lp.get("total_frs", len(fr_rows))
        certified = lp.get("certified_frs")
        recovery.append({**base, "loop": lp.get("loop", ""),
                         "targeted_features": ";".join(lp.get("targeted") or []),
                         "reproved_features": ";".join(lp.get("reproved") or []),
                         "still_failing_features": ";".join(lp.get("still_failing") or []),
                         "proved_frs": lp.get("proved_frs", ""), "certified_frs": certified,
                         "residual_frs": total - certified if isinstance(total, int) and isinstance(certified, int) else "",
                         "total_frs": total, "passver_numerator": certified,
                         "passver_denominator": total, "PassVer@1": lp.get("passver_at_1", ""),
                         "pass_at_1": lp.get("pass_at_1", ""),
                         "case_pass_rate": lp.get("case_pass_rate", "")})
    return fr_rows, stages, recovery


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", type=Path)
    args = p.parse_args()
    runs = json.loads(args.manifest.read_text())["runs"]
    rows = [summarize(r) for r in runs]

    # reference noise band per subject×language (spread over reps)
    band = defaultdict(list)
    for x in rows:
        if x["arm"] == "reference" and x["status"] == "complete" and x.get("PassVer@1") != "":
            band[(x["subject"], x["language"])].append(float(x["PassVer@1"]))
    for (subj, lang), vals in sorted(band.items()):
        if len(vals) >= 2:
            rows.append({**{k: "" for k in FIELDS}, "subject": subj, "language": lang,
                         "arm": "reference_noise_band", "status": "derived",
                         "PassVer@1": round(statistics.mean(vals), 4),
                         "PassVer@1_sd": round(statistics.pstdev(vals), 4),
                         "reference_repeats": len(vals)})

    dest = args.manifest.with_name("ablation_results.csv")
    write_csv(dest, FIELDS, rows)
    details = [detail_rows(r) for r, row in zip(runs, rows) if row["status"] == "complete"]
    for name, fields, idx in (("ablation_fr_labels.csv", FR_FIELDS, 0),
                              ("ablation_stages.csv", STAGE_FIELDS, 1),
                              ("ablation_recovery.csv", RECOVERY_FIELDS, 2)):
        write_csv(args.manifest.with_name(name), fields, [item for group in details for item in group[idx]])
    counts = defaultdict(int)
    for r in rows:
        counts[r["status"]] += 1
    print(f"Wrote {dest} ({len(rows)} rows); " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
