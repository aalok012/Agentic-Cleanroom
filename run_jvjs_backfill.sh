#!/usr/bin/env bash
# Backfill the java + js cells with the cost-control default: DeepSeek only.
# Idempotent: skips every COMPLETE cell. java + js in parallel; final CSV rebuild.
set -u
cd "$(dirname "$0")"
export MATRIX_MODELS="deepseek/deepseek-v3.2"
echo "############ java+js backfill START: $(date) ############"
./run_matrix.sh java spring        > outputs/backfill_java.log 2>&1 &
J=$!
./run_matrix.sh javascript express > outputs/backfill_js.log   2>&1 &
S=$!
echo "launched: java=$J js=$S"
wait $J $S
echo "############ backfill finished: $(date) — final CSV rebuild ############"
uv run python scripts/collect_metrics.py --root outputs/matrix --out experiment_metrics.csv
echo "experiment_metrics.csv rebuilt."
