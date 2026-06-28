#!/usr/bin/env bash
# Baseline matrix runner — the NAIVE (contract-free) pipeline across every language × SRS.
# Mirrors run_matrix.sh but calls run_baseline.py and loops all 3 languages. Models run
# CONCURRENTLY within each (language, SRS); idempotent (skips cells that already completed).
#
# Output:  outputs/baseline/<language>/<srs_stem>/<model_safe>/   (separate from the full-pipeline)
# Metrics: baseline_metrics.csv  (separate from experiment_metrics.csv; same columns)
#
# Launch detached:
#   caffeinate -i nohup ./run_baseline_matrix.sh > outputs/baseline_matrix.log 2>&1 &
set -u
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1

BASE="outputs/baseline"
CSV="baseline_metrics.csv"
LANGUAGES=(python java javascript)

if [ -n "${MATRIX_MODELS:-}" ]; then
  read -r -a MODELS <<< "$MATRIX_MODELS"
else
  MODELS=(
    "deepseek/deepseek-v3.2"
  )
fi
SRS_FILES=(data/srs/*.xml)

echo "=== baseline matrix START: $(date) ==="
echo "languages: ${LANGUAGES[*]}"
echo "models (${#MODELS[@]}): ${MODELS[*]}"
echo "srs (${#SRS_FILES[@]}): ${SRS_FILES[*]}"
echo "total cells: $(( ${#LANGUAGES[@]} * ${#MODELS[@]} * ${#SRS_FILES[@]} ))"
echo

OK=0; FAIL=0; SKIP=0
for LANG in "${LANGUAGES[@]}"; do
  echo "############ LANGUAGE: $LANG ############"
  for SRS in "${SRS_FILES[@]}"; do
    [ -e "$SRS" ] || { echo "!! no SRS files matched"; break; }
    STEM=$(basename "$SRS" .xml)
    if [ "${SEQUENTIAL:-0}" = "1" ]; then
      echo ">>> [$(date +%H:%M:%S)] $LANG / $STEM — ${#MODELS[@]} models SEQUENTIALLY (rate-limit safe)"
    else
      echo ">>> [$(date +%H:%M:%S)] $LANG / $STEM — ${#MODELS[@]} models in parallel"
    fi
    declare -a PIDS NAMES; PIDS=(); NAMES=()
    for M in "${MODELS[@]}"; do
      SAFE=$(echo "$M" | tr '/:.' '___')
      OUT="$BASE/$LANG/$STEM/$SAFE"
      if grep -lq '"status": "complete"' "$OUT"/runs/*.json 2>/dev/null; then
        echo "      skip    $LANG/$STEM × $M (already complete)"; SKIP=$((SKIP+1)); continue
      fi
      mkdir -p "$OUT"
      echo "      launch  $LANG/$STEM × $M -> $OUT/run.log"
      uv run python run_baseline.py "$SRS" --model "$M" --language "$LANG" \
        --output-dir "$OUT" > "$OUT/run.log" 2>&1 &
      PID=$!; PIDS+=($PID); NAMES+=("$M")
      # In sequential mode, wait for this model to finish before launching the next.
      if [ "${SEQUENTIAL:-0}" = "1" ]; then
        if wait "$PID"; then echo "    [$(date +%H:%M:%S)] OK    $LANG/$STEM × $M"; OK=$((OK+1))
        else echo "    [$(date +%H:%M:%S)] FAIL  $LANG/$STEM × $M (see run.log)"; FAIL=$((FAIL+1)); fi
      fi
    done
    if [ "${SEQUENTIAL:-0}" != "1" ]; then
      for i in "${!PIDS[@]}"; do
        if wait "${PIDS[$i]}"; then echo "    [$(date +%H:%M:%S)] OK    $LANG/$STEM × ${NAMES[$i]}"; OK=$((OK+1))
        else echo "    [$(date +%H:%M:%S)] FAIL  $LANG/$STEM × ${NAMES[$i]} (see run.log)"; FAIL=$((FAIL+1)); fi
      done
    fi
    uv run python scripts/collect_metrics.py --root "$BASE" --out "$CSV" || true
    echo
  done
done

uv run python scripts/collect_metrics.py --root "$BASE" --out "$CSV" || true
echo "=== baseline matrix DONE: $(date)  (ok=$OK fail=$FAIL skip=$SKIP) ==="
echo "Metrics: $CSV"
