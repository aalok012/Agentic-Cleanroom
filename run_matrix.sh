#!/usr/bin/env bash
# Experiment matrix runner — runs EVERY SRS against EVERY model, completely hands-off.
# One full pipeline per (SRS × model) cell. Within each SRS the models run CONCURRENTLY
# (max ${#MODELS[@]} parallel); SRS groups run one after another.
#
# Layout: each cell gets its own isolated output dir + ledger, so nothing collides:
#   outputs/<language>/<srs_stem>/<model_safe>/
#     ├── runs/<run_id>.json   <- per-run metrics (picked up by collect_metrics.py)
#     ├── ledger.md            <- per-cell markdown ledger
#     ├── run.log              <- full stdout/stderr for this cell
#     └── generated/           <- generated code / dafny / tests
#
# After every cell (and once at the end) it rebuilds the unified CSV in the repo root:
#   experiment_metrics.csv   <- one row per run, accumulates across ALL languages
#
# A failing cell logs FAIL and the batch keeps going — the pipeline still records
# partial metrics for it.
#
# Phase 1 (Python/FastAPI) is the default. Reuse for other stacks with args:
#   ./run_matrix.sh                 # python fastapi (default)
#   ./run_matrix.sh java spring     # Java / Spring Boot
# NOTE: the pipeline only supports languages python & java today; JS/MERN needs a
# pipeline target added first.
#
# Launch detached, kept awake, surviving terminal close:
#   caffeinate -i nohup ./run_matrix.sh > outputs/python_matrix.log 2>&1 &
# Watch:
#   tail -f outputs/python_matrix.log
#   tail -f outputs/python/<srs>/<model>/run.log
set -u
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1   # stream each run's log live (no stdout buffering)

LANGUAGE="${1:-python}"
STACK="${2:-fastapi}"
# --max-cert-loops 4: recovery loop capped at 4. --prove-rounds 4: Dafny generate→verify→revise
# iteration loop capped at 4 (was the default 6).
FLAGS="--prove --certify --max-cert-loops 4 --prove-rounds 4"
BASE="outputs/matrix"   # isolated from historical outputs/ so the CSV holds ONLY matrix runs
CSV="experiment_metrics.csv"

# Cost-control default: DeepSeek only. Override deliberately with:
#   MATRIX_MODELS="m1 m2 m3" ./run_matrix.sh ...
if [ -n "${MATRIX_MODELS:-}" ]; then
  read -r -a MODELS <<< "$MATRIX_MODELS"
else
  MODELS=(
    "deepseek/deepseek-v3.2"
  )
fi

# All SRS in data/srs/ are run (drop a new .xml in there and it's picked up automatically).
SRS_FILES=(data/srs/*.xml)

echo "=== matrix batch START: $(date) ==="
echo "language=$LANGUAGE  stack=$STACK  flags=$FLAGS"
echo "models  (${#MODELS[@]}): ${MODELS[*]}"
echo "srs     (${#SRS_FILES[@]}): ${SRS_FILES[*]}"
echo "total cells: $(( ${#MODELS[@]} * ${#SRS_FILES[@]} ))"
echo

OK=0; FAIL=0; SKIP=0; GROUP=0; TOTAL=$(( ${#MODELS[@]} * ${#SRS_FILES[@]} ))
# Models run CONCURRENTLY within each SRS (safe: each cell has its own --output-dir
# and PIPELINE_LEDGER_FILE, so generated code / dafny / ledgers never collide). We move
# to the next SRS only after all of that SRS's models finish — caps concurrency at
# ${#MODELS[@]} API streams, which is gentle on OpenRouter rate limits.
for SRS in "${SRS_FILES[@]}"; do
  [ -e "$SRS" ] || { echo "!! no SRS files matched data/srs/*.xml"; break; }
  STEM=$(basename "$SRS" .xml)
  GROUP=$((GROUP+1))
  echo ">>> [$(date +%H:%M:%S)] SRS group $GROUP/${#SRS_FILES[@]}: $STEM — launching ${#MODELS[@]} models in parallel"
  declare -a PIDS NAMES
  PIDS=(); NAMES=()
  for M in "${MODELS[@]}"; do
    SAFE=$(echo "$M" | tr '/:.' '___')
    OUT="$BASE/$LANGUAGE/$STEM/$SAFE"
    # Idempotent resume: skip a cell that already has a COMPLETE run record.
    if grep -lq '"status": "complete"' "$OUT"/runs/*.json 2>/dev/null; then
      echo "      skip    $STEM × $M  (already complete)"; SKIP=$((SKIP+1)); continue
    fi
    mkdir -p "$OUT"
    echo "      launch  $STEM × $M  -> $OUT/run.log"
    PIPELINE_LEDGER_FILE="$OUT/ledger.md" \
      uv run python run_pipeline.py "$SRS" \
        --model "$M" --language "$LANGUAGE" --stack "$STACK" $FLAGS \
        --output-dir "$OUT" > "$OUT/run.log" 2>&1 &
    PIDS+=($!); NAMES+=("$M")
  done
  for i in "${!PIDS[@]}"; do
    if wait "${PIDS[$i]}"; then
      echo "    [$(date +%H:%M:%S)] OK    $STEM × ${NAMES[$i]}"; OK=$((OK+1))
    else
      echo "    [$(date +%H:%M:%S)] FAIL  $STEM × ${NAMES[$i]}  (see run.log; partial metrics recorded)"; FAIL=$((FAIL+1))
    fi
  done
  # Rebuild the unified CSV after each SRS group so progress is durable even if interrupted.
  uv run python scripts/collect_metrics.py --root "$BASE" --out "$CSV" || true
  echo
done

uv run python scripts/collect_metrics.py --root "$BASE" --out "$CSV" || true
echo "=== matrix batch DONE: $(date)  (ok=$OK fail=$FAIL skip=$SKIP of $TOTAL) ==="
echo "Unified metrics: $CSV"
