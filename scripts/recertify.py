"""Re-run pass@k certification against EXISTING proved artifacts (never re-proves).

Loads a finished run's enriched IR, reuses its generated tests, restages the proved Dafny cores,
and re-scores the un-proved features. n=1 is FREE (only the pipeline code sample, no LLM); n>1
generates the extra samples with the default model (gpt-4o-mini) — cheap, and tokens are logged.

Usage:  uv run python scripts/recertify.py [outputs/<stem>_full_ir.json] [n]
"""

import json
import re
import sys
from pathlib import Path

from src.cleanroom.agents.evaluation.agent import CertificationAgent
from src.cleanroom.llms.callbacks.metric import GLOBAL_METRICS
from src.cleanroom.utils.cost import estimate_cost_by_model
from src.cleanroom.utils.usage_log import append_usage_log


def _fix_adapter_mangling(generated_code: dict) -> int:
    """Idempotently apply the Dafny `_`->`__` module-name mangling to adapter imports."""
    fixed = 0
    for f in generated_code.get("files", []):
        if f.get("path", "").endswith("_adapter.py"):
            new = re.sub(r"import (F\d+)_(\d+)Domain", r"import \1__\2Domain", f["content"])
            if new != f["content"]:
                f["content"] = new
                fixed += 1
    return fixed


def main() -> None:
    ir_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs/dineout_srs_full_ir.json")
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    ir = json.loads(ir_path.read_text())

    proved = ir.get("proved_feature_ids") or []
    if not (ir.get("generated_code") and ir.get("generated_tests")):
        sys.exit("IR has no generated_code/generated_tests — run the pipeline first.")
    proved_modules = [f"F{p.replace('.', '_')}" for p in proved]
    proj = Path("outputs/generated") / ir["project_name"] / "dafny_proof"
    k_values = tuple(sorted({1, n}))

    n_fixed = _fix_adapter_mangling(ir["generated_code"])
    print(f"IR        : {ir_path}")
    print(f"Stack     : {ir.get('stack')}   proved (skipped): {proved or '(none)'}")
    print(f"Samples   : n={n}  (sample 0 is the existing pipeline code; {max(0, n - 1)} generated with gpt-4o-mini)")
    print(f"Adapters fixed for Dafny name-mangling: {n_fixed}")

    agent = CertificationAgent(
        stack=ir.get("stack", "fastapi"), n=n, k_values=k_values, use_pipeline_sample=True,
        skip_feature_ids=set(proved),
        dafny_proj=proj if proved else None,
        dafny_modules=proved_modules if proved else None,
    )
    res = agent.certify(ir)

    kcols = sorted(res.aggregate_pass_at)
    print("\n=== pass@k for the UN-proved features ===")
    for fr in res.frs:
        ks = "  ".join(f"{k}={fr.pass_at.get(k, 0):.2f}" for k in kcols)
        print(f"  {fr.fr_id:16s} {ks}  cases {fr.cases_passed}/{fr.cases_total}")
    agg = "  ".join(f"{k}={res.aggregate_pass_at[k]:.3f}" for k in kcols)
    print(f"\naggregate {agg}  case_rate={res.aggregate_case_pass_rate:.3f}  ({len(res.frs)} un-proved FR(s))")

    # Log usage honestly — free for n=1, real per-model cost for n>1.
    in_tot, out_tot, calls = GLOBAL_METRICS.snapshot()
    cost, by_model = estimate_cost_by_model(GLOBAL_METRICS.calls)
    model = "+".join(sorted(by_model)) if by_model else "none (free re-cert)"
    metrics = {
        "srs": ir_path.name, "stack": ir.get("stack"), "model": model, "total_seconds": 0.0,
        "tokens": {"input": in_tot, "output": out_tot, "total": in_tot + out_tot, "calls": calls},
        "cost_usd": cost, "cost_by_model": by_model,
    }
    append_usage_log(metrics, status=f"recertify@{n}", run_id=f"recertify-{ir_path.stem}-n{n}")
    print(f"\nLogged to API_USAGE.md: {calls} LLM call(s), {in_tot + out_tot:,} tokens, ${cost:.4f}.")


if __name__ == "__main__":
    main()
