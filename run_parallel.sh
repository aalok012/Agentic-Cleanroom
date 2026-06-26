#!/usr/bin/env bash
# Parallel pipeline runner — runs several models AT THE SAME TIME, each in its own output dir
# and its own ledger, then merges the per-run ledgers into the master comparison file.
#
# Safe to parallelize because: (1) each run gets a separate --output-dir, so generated code /
# Dafny / the runnable app never collide; (2) each run writes its own ledger via
# PIPELINE_LEDGER_FILE, so concurrent appends can't interleave — they're merged at the end.
#
# The pipeline is I/O-bound (waiting on the API + the dafny subprocess), so N models in parallel
# finish in roughly the time of the SLOWEST single model, not the sum.
#
# Usage:
#   ./run_parallel.sh                 # runs the MODELS list below, waits, merges
#   nohup ./run_parallel.sh > outputs/parallel/_driver.log 2>&1 &   # detached
#
# Watch a single model live:   tail -f outputs/parallel/<model>/run.log
set -u
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1   # stream each run's log live (no stdout buffering)

SRS="data/srs/dineout_srs.xml"
FLAGS="--prove --certify --max-cert-loops 6 --stack fastapi"
BASE="outputs/parallel"
MASTER="Full_Pipeline_run_metric_record_with_differentModels.md"
mkdir -p "$BASE"

# Models to run concurrently — edit freely. Mind OpenRouter per-key rate limits (3-5 is usually fine).
MODELS=(
  "deepseek/deepseek-v4-pro"
  "qwen/qwen3-max"
  "moonshotai/kimi-k2-thinking"
)

declare -a PIDS NAMES
echo "=== parallel batch START: $(date) ==="
for M in "${MODELS[@]}"; do
  SAFE=$(echo "$M" | tr '/:.' '___')
  OUT="$BASE/$SAFE"
  mkdir -p "$OUT"
  echo ">>> launch $M  ->  $OUT  (log: $OUT/run.log)"
  PIPELINE_LEDGER_FILE="$OUT/ledger.md" \
    uv run python run_pipeline.py "$SRS" --model "$M" $FLAGS \
      --output-dir "$OUT" > "$OUT/run.log" 2>&1 &
  PIDS+=($!)
  NAMES+=("$M")
done

echo "launched ${#PIDS[@]} runs (pids: ${PIDS[*]}); waiting for all to finish..."
FAILS=0
for i in "${!PIDS[@]}"; do
  if wait "${PIDS[$i]}"; then echo "    OK    ${NAMES[$i]}"
  else echo "    FAIL  ${NAMES[$i]} (see its run.log; partial recorded)"; FAILS=$((FAILS+1)); fi
done

# Merge each run's ledger into the master (skip duplicate title headers; keep section bodies).
echo "=== merging ledgers into $MASTER ==="
if [ ! -f "$MASTER" ]; then
  printf '# Full pipeline — run metrics across different models\n\n_Merged from parallel runs._\n\n' > "$MASTER"
fi
for M in "${MODELS[@]}"; do
  SAFE=$(echo "$M" | tr '/:.' '___')
  L="$BASE/$SAFE/ledger.md"
  [ -f "$L" ] && sed -n '/^---/,$p' "$L" >> "$MASTER"
done

echo "=== parallel batch DONE: $(date)  ($FAILS failed) ==="
echo "Master ledger: $MASTER"
