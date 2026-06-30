#!/usr/bin/env bash
# Re-run the TWO fixed SRS (kinmail + video search) across ALL models and ALL languages,
# with the new finer feature extraction, into an ISOLATED output root + its own CSV so the
# main experiment (outputs/matrix / experiment_metrics.csv) is left untouched.
#
#   - 2 SRS x 3 languages x 4 models = 24 cells
#   - concurrency: MAXJOBS cells in flight at once (default 3), spanning different models
#   - CHECKPOINTED: a cell with an existing "status": "complete" run record is skipped, and
#     the CSV is rebuilt periodically — so the script is safe to Ctrl-C and re-run (resumes).
#
# Launch (detached, survives logout):
#   caffeinate -i nohup ./scripts/run_fixed_two_srs.sh > outputs/fixed_two_srs.log 2>&1 &
set -u
cd "$(dirname "$0")/.."

MODELS=(
  "deepseek/deepseek-v3.2"
  "google/gemini-3.1-pro-preview"
  "anthropic/claude-sonnet-4-6"
  "openai/gpt-5.1"
)
SRS_FILES=(
  "data/srs/kinmail_srs.xml"
  "data/srs/2009 - video search.xml"
)
LANGS=( "python:fastapi" "java:spring" "javascript:express" )

BASE="outputs/matrix_fixed"
CSV="experiment_metrics_fixed.csv"
FLAGS="--prove --certify --max-cert-loops 4 --prove-rounds 4"
MAXJOBS="${MAXJOBS:-3}"

checkpoint() { uv run python scripts/collect_metrics.py --root "$BASE" --out "$CSV" >/dev/null 2>&1 || true; }

run_cell() {
  local SRS="$1" STEM="$2" LANG="$3" STACK="$4" M="$5"
  local SAFE OUT
  SAFE=$(echo "$M" | tr '/:.' '___')
  OUT="$BASE/$LANG/$STEM/$SAFE"
  if grep -lq '"status": "complete"' "$OUT"/runs/*.json 2>/dev/null; then
    echo "  [skip done] $STEM | $LANG | $M"; return 0
  fi
  mkdir -p "$OUT"
  echo "  [launch] $STEM | $LANG | $M -> $OUT/run.log"
  PIPELINE_LEDGER_FILE="$OUT/ledger.md" \
    uv run python run_pipeline.py "$SRS" \
      --model "$M" --language "$LANG" --stack "$STACK" $FLAGS \
      --output-dir "$OUT" > "$OUT/run.log" 2>&1
  echo "  [done $?] $STEM | $LANG | $M"
}

# Build the full cell list (SRS x language x model).
CELLS=()
for SRS in "${SRS_FILES[@]}"; do
  STEM=$(basename "$SRS" .xml)
  for LS in "${LANGS[@]}"; do
    LANG="${LS%%:*}"; STACK="${LS##*:}"
    for M in "${MODELS[@]}"; do
      CELLS+=("$SRS|$STEM|$LANG|$STACK|$M")
    done
  done
done

echo "=== fixed-extraction re-run START: $(date) ==="
echo "cells: ${#CELLS[@]}  concurrency: $MAXJOBS  base: $BASE  csv: $CSV"
checkpoint   # write the seeded cells immediately as the first checkpoint

for CELL in "${CELLS[@]}"; do
  IFS='|' read -r SRS STEM LANG STACK M <<< "$CELL"
  # throttle: wait while MAXJOBS cells are running; checkpoint the CSV as we wait
  while [ "$(jobs -rp | wc -l | tr -d ' ')" -ge "$MAXJOBS" ]; do
    sleep 15; checkpoint
  done
  run_cell "$SRS" "$STEM" "$LANG" "$STACK" "$M" &
done

wait
checkpoint
echo "=== fixed-extraction re-run DONE: $(date) -> $CSV ==="
