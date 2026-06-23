"""Re-prove ONLY the currently-unproved features against an existing run — cheaper than re-running
the whole pipeline. Picks up the strengthened proof tactics in DafnyAgent and re-attempts each
failed feature, then compiles any newly-proved ones and updates the IR. Spends gpt-4.1 tokens
(logged to API_USAGE.md).

Usage:  uv run python scripts/reprove.py [outputs/<stem>_full_ir.json] [max_rounds] [fid ...]
"""

import json
import sys
from pathlib import Path

from src.cleanroom.agents.dafny.agent import DafnyAgent
from src.cleanroom.agents.dafny.schema.dafny import FeatureDafny, GeneratedDafny
from src.cleanroom.llms.callbacks.metric import GLOBAL_METRICS
from src.cleanroom.utils.cost import estimate_cost_by_model
from src.cleanroom.utils.dafny_project import compile_dafny, scaffold_dafny_project
from src.cleanroom.utils.usage_log import append_usage_log

_MODEL = "gpt-4.1"


def main() -> None:
    ir_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs/dineout_srs_full_ir.json")
    max_rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ir = json.loads(ir_path.read_text())
    gd = ir.get("generated_dafny") or {}
    feats = {f["feature_id"]: f for f in gd.get("features", [])}

    targets = sys.argv[3:] or [fid for fid, f in feats.items() if not f["verified"]]
    if not targets:
        sys.exit("nothing to re-prove (no unproved features).")

    proj = Path("outputs/generated") / ir["project_name"] / "dafny_proof"
    if not (proj / "dafny" / "Replay.dfy").exists():
        scaffold_dafny_project(proj)
    agent = DafnyAgent(proj, model=_MODEL, max_rounds=max_rounds)

    print(f"IR        : {ir_path}")
    print(f"Re-proving: {sorted(targets)}   (max_rounds={max_rounds}, model={_MODEL})\n")
    results: list[FeatureDafny] = []
    for fid in sorted(targets):
        r = agent.generate_feature(ir, fid)
        results.append(r)
        ax = f"  [{len(r.axioms)} axiom(s)]" if r.axioms else ""
        print(f"  [{fid}] {'PROVED ' if r.verified else 'still unproved'}  ({r.rounds}r){ax}")
        if not r.verified and r.residual_errors:
            print(f"        residual: {r.residual_errors[0].get('message','')[:90]}")

    # Merge results back into the IR + recompile the newly proved.
    newly = [r for r in results if r.verified]
    for r in results:
        feats[r.feature_id] = {"feature_id": r.feature_id, "module": r.module,
                               "verified": r.verified, "rounds": r.rounds, "axioms": len(r.axioms)}
        for src in gd.get("features", []):
            if src["feature_id"] == r.feature_id:
                src.update(feats[r.feature_id]); break
    if newly:
        compile_dafny(proj, GeneratedDafny(features=newly), target=ir.get("config", {}).get("prove_target", "py"))
    proved = sorted(fid for fid, f in feats.items() if f["verified"])
    ir["proved_feature_ids"] = proved
    ir_path.write_text(json.dumps(ir, indent=2))

    print(f"\nNewly proved: {[r.feature_id for r in newly] or '(none)'}")
    print(f"Total proved now: {len(proved)}/{len(feats)}  → {proved}")
    print(f"IR updated: {ir_path}")

    # Log gpt-4.1 usage.
    in_tot, out_tot, calls = GLOBAL_METRICS.snapshot()
    cost, by_model = estimate_cost_by_model(GLOBAL_METRICS.calls)
    metrics = {
        "srs": ir_path.name, "stack": ir.get("stack"),
        "model": "+".join(sorted(by_model)) if by_model else _MODEL, "total_seconds": 0.0,
        "tokens": {"input": in_tot, "output": out_tot, "total": in_tot + out_tot, "calls": calls},
        "cost_usd": cost, "cost_by_model": by_model,
    }
    append_usage_log(metrics, status="reprove", run_id=f"reprove-{ir_path.stem}")
    print(f"Logged to API_USAGE.md: {calls} call(s), {in_tot + out_tot:,} tokens, ${cost:.4f}.")


if __name__ == "__main__":
    main()
