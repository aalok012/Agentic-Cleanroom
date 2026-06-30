#!/usr/bin/env bash
# Add foodsaver to the experiment matrix on GPT-5.1 (deepseek foodsaver already ingested into
# outputs/matrix/<lang>/foodsaver/deepseek_deepseek-v3_2 from the earlier foodsaver_lang run).
#
# 3 cells: foodsaver | gpt-5.1 | python / java / javascript -> outputs/matrix/<lang>/foodsaver/openai_gpt-5_1
#
# Writes its progress CSV to experiment_metrics_foodsaver.csv (NOT experiment_metrics.csv) so it
# never races the concurrently-running Shoten driver, which owns experiment_metrics.csv. A final
# authoritative `collect_metrics --root outputs/matrix --out experiment_metrics.csv` (run once both
# drivers are done) folds everything together.
set -u
cd "$(dirname "$0")/.."
export CLEANROOM_LLM_MAX_RETRIES="${CLEANROOM_LLM_MAX_RETRIES:-6}"
export CLEANROOM_LLM_TIMEOUT="${CLEANROOM_LLM_TIMEOUT:-180}"

MODEL="openai/gpt-5.1"; MDIR="openai_gpt-5_1"
SRS="data/srs/foodsaver.xml"
MAX_PARALLEL="${MAX_PARALLEL:-3}"
RETRY_WAIT=120; MAX_ATTEMPTS=5
CSV="experiment_metrics_foodsaver.csv"

rebuild() { uv run python scripts/collect_metrics.py --root outputs/matrix --out "$CSV" >/dev/null 2>&1 || true; }

run_cell() {
  local lang="$1" stack="$2"
  local out="outputs/matrix/${lang}/foodsaver/${MDIR}"
  mkdir -p "$out"
  local attempt rc=1
  for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
    echo "[fs-gpt51] START foodsaver | ${lang}/${stack} | attempt ${attempt}/${MAX_ATTEMPTS} $(date)"
    uv run python run_pipeline.py "$SRS" \
        --language "$lang" --stack "$stack" --model "$MODEL" \
        --prove --certify --samples 1 --resume \
        --output-dir "$out" > "${out}/run.log" 2>&1
    rc=$?
    echo "[fs-gpt51] DONE  foodsaver | ${lang} | attempt ${attempt} exit=${rc} $(date)"
    [ "$rc" -eq 0 ] && break
    [ "$attempt" -lt "$MAX_ATTEMPTS" ] && { echo "[fs-gpt51] ${lang} failed; ${RETRY_WAIT}s then resume…"; sleep "$RETRY_WAIT"; }
  done
  rebuild
}

throttle() { while [ "$(jobs -rp | wc -l | tr -d ' ')" -ge "$MAX_PARALLEL" ]; do sleep 10; done; }

echo "=== foodsaver gpt-5.1 START $(date)  parallel=${MAX_PARALLEL} ==="
for combo in "python:auto" "java:spring" "javascript:express"; do
  throttle
  run_cell "${combo%%:*}" "${combo##*:}" &
  sleep 3
done
wait
rebuild
echo "=== foodsaver gpt-5.1 DONE $(date) ==="
