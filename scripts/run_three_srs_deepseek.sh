#!/usr/bin/env bash
# Run THREE newly-parseable SRS (G16, trading SRS, Shoten) through the FULL pipeline
# (--prove --certify) on DeepSeek only, across all three languages, into the matrix layout
# experiment_metrics.csv aggregates: outputs/matrix/<lang>/<srs_stem>/<model_safe>/runs/<id>.json.
#
# Cells run SEQUENTIALLY (the repo's anti-concurrency lesson); each uses --resume so a transient
# OpenRouter blip resumes from the failed stage. On a non-zero exit a cell WAITS 120s then retries
# (up to 3 attempts total). The CSV is rebuilt (idempotent) after every cell so results accrue live.
set -u
cd "$(dirname "$0")/.."

export CLEANROOM_LLM_MAX_RETRIES="${CLEANROOM_LLM_MAX_RETRIES:-6}"
export CLEANROOM_LLM_TIMEOUT="${CLEANROOM_LLM_TIMEOUT:-180}"

MODEL="deepseek/deepseek-v3.2"
MODELDIR="deepseek_deepseek-v3_2"
RETRY_WAIT=120          # seconds to wait before retrying a failed cell
MAX_ATTEMPTS=5          # generous for unattended overnight runs (transient OpenRouter 500s)

run_cell () {
  local srs="$1" lang="$2" stack="$3"
  local stem; stem="$(basename "$srs" .xml)"
  local out="outputs/matrix/${lang}/${stem}/${MODELDIR}"
  mkdir -p "$out"
  local attempt rc
  for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
    echo "[3srs] === ${stem} | ${lang}/${stack} | attempt ${attempt}/${MAX_ATTEMPTS} -> ${out} ==="
    uv run python run_pipeline.py "$srs" \
        --language "$lang" --stack "$stack" --model "$MODEL" \
        --prove --certify --samples 1 --resume \
        --output-dir "$out" > "${out}/run.log" 2>&1
    rc=$?
    echo "[3srs] ${stem}/${lang} attempt ${attempt} exit=${rc}"
    [ "$rc" -eq 0 ] && break
    if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
      echo "[3srs] ${stem}/${lang} failed; waiting ${RETRY_WAIT}s then retrying (resume)..."
      sleep "$RETRY_WAIT"
    fi
  done
  # APPEND-only: keep every existing CSV row, just add this new cell (update if re-run). Never rebuilds.
  uv run python scripts/collect_metrics.py --append --root outputs/matrix --out experiment_metrics.csv
  echo "[3srs] CSV appended after ${stem}/${lang} (exit ${rc})"
}

# Smallest SRS first (quick CSV wins); the 54-FR Shoten last.
for SRS in \
    "data/srs/G16-SRS.xml" \
    "data/srs/SRS (Software Requirement Specification).xml" \
    "data/srs/Shoten_SRS.xml"; do
  run_cell "$SRS" python     auto
  run_cell "$SRS" java       spring
  run_cell "$SRS" javascript express
done
echo "[3srs] all 9 cells complete."
