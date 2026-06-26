#!/usr/bin/env bash
# Overnight batch runner — runs the full pipeline once per model, completely hands-off.
# Each run appends a section to Full_Pipeline_run_metric_record_with_differentModels.md and
# writes its own log under outputs/overnight/. A failing run does NOT stop the batch — its
# partial metrics are still recorded, and the next model runs.
#
# Launch (stays awake + survives closing the terminal):
#   caffeinate -i nohup ./run_overnight.sh > outputs/overnight/_batch.log 2>&1 &
#
# Watch progress in the morning:
#   tail -n 50 outputs/overnight/_batch.log
#   cat Full_Pipeline_run_metric_record_with_differentModels.md
set -u
cd "$(dirname "$0")"

SRS="data/srs/dineout_srs.xml"
FLAGS="--prove --certify --max-cert-loops 6 --stack fastapi"
LOGDIR="outputs/overnight"
mkdir -p "$LOGDIR"

# One full pipeline run per model, top to bottom. Edit this list as you like.
# Reliable (closed) models are first so you wake up to at least one complete run.
MODELS=(
  "openai/gpt-5.5"
  "google/gemini-3.1-pro-preview"
  "deepseek/deepseek-chat"
  "qwen/qwen3-coder"
  "openai/gpt-4o-mini"
)

echo "=== overnight batch START: $(date) ==="
echo "SRS=$SRS  FLAGS=$FLAGS"
echo "models: ${MODELS[*]}"
echo

for M in "${MODELS[@]}"; do
  TS=$(date +%Y%m%d-%H%M%S)
  SAFE=$(echo "$M" | tr '/:' '__')
  LOG="$LOGDIR/${TS}_${SAFE}.log"
  echo ">>> [$(date +%H:%M:%S)] START model=$M   (log: $LOG)"
  if uv run python run_pipeline.py "$SRS" --model "$M" $FLAGS > "$LOG" 2>&1; then
    echo "    [$(date +%H:%M:%S)] OK    $M"
  else
    echo "    [$(date +%H:%M:%S)] FAIL  $M  (see $LOG; partial recorded in ledger)"
  fi
  echo
done

echo "=== overnight batch DONE: $(date) ==="
echo "Results: Full_Pipeline_run_metric_record_with_differentModels.md"
