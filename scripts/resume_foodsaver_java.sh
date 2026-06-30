#!/usr/bin/env bash
# Re-run the foodsaver java/spring cell with --resume until it completes, retrying transient
# OpenRouter 500s (up to 5 attempts, 120s apart). Separate output dir from the 3-SRS matrix, so
# the two streams never collide. Mirrors the 3-SRS driver's retry policy.
set -u
cd "$(dirname "$0")/.."
export CLEANROOM_LLM_MAX_RETRIES="${CLEANROOM_LLM_MAX_RETRIES:-6}"
export CLEANROOM_LLM_TIMEOUT="${CLEANROOM_LLM_TIMEOUT:-180}"

out="outputs/foodsaver_lang/java"
rc=1
for attempt in 1 2 3 4 5; do
  echo "[java-resume] attempt ${attempt}/5 starting $(date)" | tee -a "${out}/run_resume.log"
  uv run python run_pipeline.py data/srs/foodsaver.xml \
      --language java --stack spring --prove --certify --samples 1 --resume \
      --output-dir "$out" >> "${out}/run_resume.log" 2>&1
  rc=$?
  echo "[java-resume] attempt ${attempt} exit=${rc} $(date)" | tee -a "${out}/run_resume.log"
  [ "$rc" -eq 0 ] && break
  [ "$attempt" -lt 5 ] && { echo "[java-resume] waiting 120s then retrying..."; sleep 120; }
done
echo "[java-resume] FINAL exit=${rc} $(date)" | tee -a "${out}/run_resume.log"
