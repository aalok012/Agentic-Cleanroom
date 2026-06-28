#!/usr/bin/env bash
# Re-run DeepSeek for a SINGLE SRS into the matrix layout. Used to backfill cells
# that failed earlier (e.g. an SRS that the parser couldn't read until it was fixed).
#
# It does NOT rebuild the CSV — the main run_matrix.sh/run_all_matrix.sh collector scans all
# of outputs/matrix and will pick these up on its next pass (avoids a concurrent-write race).
#
# Usage:
#   ./rerun_cells.sh <language> <stack> "<srs_file>"
#   ./rerun_cells.sh python fastapi "data/srs/0000 - cctns.xml"
#
# Launch detached:
#   caffeinate -i nohup ./rerun_cells.sh python fastapi "data/srs/0000 - cctns.xml" \
#     > outputs/rerun_cctns_python.log 2>&1 &
set -u
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1

LANGUAGE="$1"; STACK="$2"; SRS="$3"
FLAGS="--prove --certify --max-cert-loops 4 --prove-rounds 4"   # keep in sync with run_matrix.sh
BASE="outputs/matrix"
MODELS=(
  "deepseek/deepseek-v3.2"
)

STEM=$(basename "$SRS" .xml)
echo "=== rerun START: $(date)  $STEM  ($LANGUAGE/$STACK) ==="
declare -a PIDS NAMES
for M in "${MODELS[@]}"; do
  SAFE=$(echo "$M" | tr '/:.' '___')
  OUT="$BASE/$LANGUAGE/$STEM/$SAFE"
  rm -rf "$OUT"; mkdir -p "$OUT"   # clear any prior failed attempt for a clean row
  echo "  launch  $STEM × $M  -> $OUT/run.log"
  PIPELINE_LEDGER_FILE="$OUT/ledger.md" \
    uv run python run_pipeline.py "$SRS" \
      --model "$M" --language "$LANGUAGE" --stack "$STACK" $FLAGS \
      --output-dir "$OUT" > "$OUT/run.log" 2>&1 &
  PIDS+=($!); NAMES+=("$M")
done
for i in "${!PIDS[@]}"; do
  if wait "${PIDS[$i]}"; then echo "  OK    $STEM × ${NAMES[$i]}"
  else echo "  FAIL  $STEM × ${NAMES[$i]} (see run.log)"; fi
done
echo "=== rerun DONE: $(date)  $STEM ==="
echo "Cells written under $BASE/$LANGUAGE/$STEM/ — the main collector will fold them into experiment_metrics.csv."
