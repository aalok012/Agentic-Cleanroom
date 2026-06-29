#!/usr/bin/env bash
# MoT (Module-of-Thought) prompt-strategy experiment runner.
# Runs EVERY SRS in data/srs/ across 3 languages with --prompt-strategy mot, DeepSeek only.
# Within each SRS the 3 languages run CONCURRENTLY; SRS groups run one after another.
#
# Layout (isolated from baseline outputs/): one cell per (SRS × language):
#   outputs/mot/<srs_stem>/<language>/
#     ├── runs/<run_id>.json   <- per-run metrics (collect_metrics.py picks these up)
#     ├── ledger.md            <- per-cell ledger
#     ├── run.log              <- full stdout/stderr for this cell
#     └── generated/           <- generated code / dafny / tests
#
# After each SRS finishes it writes that SRS's results CSV in the repo root, SAME columns as
# experiment_metrics.csv:
#   <srs_stem>_results_mot_deepseek.csv
set -u
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1

MODEL="deepseek/deepseek-v3.2"
# Match run_matrix.sh flags so MoT rows are comparable to the baseline matrix.
FLAGS="--prove --certify --max-cert-loops 4 --prove-rounds 4"
BASE="outputs/mot"
SRS_FILES=(data/srs/*.xml)

# (language, stack) pairs — python/fastapi, java/spring, javascript/express (auto).
LANGS=("python fastapi" "java spring" "javascript express")

echo "=== MoT matrix START: $(date) ==="
echo "model=$MODEL  strategy=mot  flags=$FLAGS"
echo "srs (${#SRS_FILES[@]}): ${SRS_FILES[*]}"
echo "cells: $(( ${#SRS_FILES[@]} * ${#LANGS[@]} ))"
echo

OK=0; FAIL=0; SKIP=0
for SRS in "${SRS_FILES[@]}"; do
  [ -e "$SRS" ] || { echo "!! no SRS files matched data/srs/*.xml"; break; }
  STEM=$(basename "$SRS" .xml)
  echo ">>> [$(date +%H:%M:%S)] SRS: $STEM — launching ${#LANGS[@]} languages in parallel"
  declare -a PIDS NAMES
  PIDS=(); NAMES=()
  for LS in "${LANGS[@]}"; do
    read -r LANG STACK <<< "$LS"
    OUT="$BASE/$STEM/$LANG"
    # Idempotent resume: skip a cell that already has a COMPLETE run record.
    if grep -lq '"status": "complete"' "$OUT"/runs/*.json 2>/dev/null; then
      echo "      skip    $STEM × $LANG  (already complete)"; SKIP=$((SKIP+1)); continue
    fi
    mkdir -p "$OUT"
    (
      PIPELINE_LEDGER_FILE="$OUT/ledger.md" \
      uv run python run_pipeline.py "$SRS" \
        --prompt-strategy mot --model "$MODEL" \
        --language "$LANG" --stack "$STACK" \
        $FLAGS --output-dir "$OUT" > "$OUT/run.log" 2>&1
    ) &
    PIDS+=($!); NAMES+=("$STEM/$LANG")
  done
  # Wait for all languages of this SRS.
  for i in "${!PIDS[@]}"; do
    if wait "${PIDS[$i]}"; then echo "      ok      ${NAMES[$i]}"; OK=$((OK+1));
    else echo "      FAIL    ${NAMES[$i]}  (see $BASE/${NAMES[$i]}/run.log)"; FAIL=$((FAIL+1)); fi
  done
  # Per-SRS CSV (3 language rows), same columns as experiment_metrics.csv.
  CSV="${STEM}_results_mot_deepseek.csv"
  uv run python scripts/collect_metrics.py --root "$BASE/$STEM" --out "$CSV" \
    && echo "      CSV     $CSV"
done

echo
echo "=== MoT matrix DONE: $(date)  ok=$OK fail=$FAIL skip=$SKIP ==="
