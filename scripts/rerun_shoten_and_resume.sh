#!/usr/bin/env bash
# Re-run Shoten (after the 17-feature srs_reader fix) and finish the pending GPT-5.1 cells
# for the trading SRS, into the matrix layout collect_metrics aggregates.
#
# Cells (9 total):
#   Shoten_SRS                              -> deepseek + gpt-5.1, all 3 languages   (FRESH: stale
#                                              15-feature deepseek dirs were moved to
#                                              outputs/_stale_backup before launch)
#   SRS (Software Requirement Specification) -> gpt-5.1, all 3 languages              (was pending)
#
# Each cell uses --resume + per-stage checkpoints, so a transient OpenRouter blip resumes from the
# failed stage. A non-zero exit waits RETRY_WAIT then retries (up to MAX_ATTEMPTS). Up to
# MAX_PARALLEL cells run at once (distinct --output-dir each, so disk never collides). The CSV is
# rebuilt from scratch (idempotent, deduped by language/srs/model) after every cell so the stale
# Shoten rows are replaced live.
#
# Launch (detached, survives logout):
#   caffeinate -i nohup ./scripts/rerun_shoten_and_resume.sh > outputs/rerun_shoten.log 2>&1 &
set -u
cd "$(dirname "$0")/.."

export CLEANROOM_LLM_MAX_RETRIES="${CLEANROOM_LLM_MAX_RETRIES:-6}"
export CLEANROOM_LLM_TIMEOUT="${CLEANROOM_LLM_TIMEOUT:-180}"

MAX_PARALLEL="${MAX_PARALLEL:-3}"
RETRY_WAIT=120
MAX_ATTEMPTS=5

# srs_file | lang | stack | model | model_dir
CELLS=(
  "data/srs/Shoten_SRS.xml|python|auto|deepseek/deepseek-v3.2|deepseek_deepseek-v3_2"
  "data/srs/Shoten_SRS.xml|java|spring|deepseek/deepseek-v3.2|deepseek_deepseek-v3_2"
  "data/srs/Shoten_SRS.xml|javascript|express|deepseek/deepseek-v3.2|deepseek_deepseek-v3_2"
  "data/srs/Shoten_SRS.xml|python|auto|openai/gpt-5.1|openai_gpt-5_1"
  "data/srs/Shoten_SRS.xml|java|spring|openai/gpt-5.1|openai_gpt-5_1"
  "data/srs/Shoten_SRS.xml|javascript|express|openai/gpt-5.1|openai_gpt-5_1"
  "data/srs/SRS (Software Requirement Specification).xml|python|auto|openai/gpt-5.1|openai_gpt-5_1"
  "data/srs/SRS (Software Requirement Specification).xml|java|spring|openai/gpt-5.1|openai_gpt-5_1"
  "data/srs/SRS (Software Requirement Specification).xml|javascript|express|openai/gpt-5.1|openai_gpt-5_1"
)

rebuild_csv() { uv run python scripts/collect_metrics.py --root outputs/matrix --out experiment_metrics.csv >/dev/null 2>&1 || true; }

run_cell() {
  local srs="$1" lang="$2" stack="$3" model="$4" mdir="$5"
  local stem; stem="$(basename "$srs" .xml)"
  local out="outputs/matrix/${lang}/${stem}/${mdir}"
  mkdir -p "$out"
  local attempt rc=1
  for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
    echo "[rerun] START ${stem} | ${lang}/${stack} | ${model} | attempt ${attempt}/${MAX_ATTEMPTS} $(date)"
    uv run python run_pipeline.py "$srs" \
        --language "$lang" --stack "$stack" --model "$model" \
        --prove --certify --samples 1 --resume \
        --output-dir "$out" > "${out}/run.log" 2>&1
    rc=$?
    echo "[rerun] DONE  ${stem} | ${lang} | ${model} | attempt ${attempt} exit=${rc} $(date)"
    [ "$rc" -eq 0 ] && break
    [ "$attempt" -lt "$MAX_ATTEMPTS" ] && { echo "[rerun] ${stem}/${lang}/${model} failed; ${RETRY_WAIT}s then resume…"; sleep "$RETRY_WAIT"; }
  done
  rebuild_csv
  echo "[rerun] CSV rebuilt after ${stem}/${lang}/${model}"
}

throttle() { while [ "$(jobs -rp | wc -l | tr -d ' ')" -ge "$MAX_PARALLEL" ]; do sleep 10; done; }

echo "=== rerun START $(date)  cells=${#CELLS[@]}  parallel=${MAX_PARALLEL} ==="
rebuild_csv
for CELL in "${CELLS[@]}"; do
  IFS='|' read -r srs lang stack model mdir <<< "$CELL"
  throttle
  run_cell "$srs" "$lang" "$stack" "$model" "$mdir" &
  sleep 3
done
wait
rebuild_csv
echo "=== rerun DONE $(date) -> experiment_metrics.csv ==="
