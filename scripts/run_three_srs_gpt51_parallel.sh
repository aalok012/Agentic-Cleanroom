#!/usr/bin/env bash
# Run THREE new SRS (G16, "SRS (Software Requirement Specification)", Shoten) through the FULL
# pipeline (--prove --certify) on GPT-5.1, across all three languages, IN PARALLEL, into the
# matrix layout collect_metrics aggregates: outputs/matrix/<lang>/<srs_stem>/<model_safe>/.
#
# Parallelism: up to MAX_PARALLEL cells run at once (portable bash-3.2 `jobs -rp` throttle — no
# `wait -n`). Each cell writes to its OWN --output-dir, so concurrent cells never collide on disk;
# only the CSV append is shared, so it runs ONCE after all cells finish (no concurrent-write race).
#
# Resilience / token-optimization: every cell uses --resume + per-stage checkpoints + the per-feature
# Dafny proof cache, so a transient OpenRouter blip resumes from the failed stage — never from scratch.
# A non-zero cell exit waits RETRY_WAIT then retries (up to MAX_ATTEMPTS) via --resume.
set -u
cd "$(dirname "$0")/.."

export CLEANROOM_LLM_MAX_RETRIES="${CLEANROOM_LLM_MAX_RETRIES:-6}"
export CLEANROOM_LLM_TIMEOUT="${CLEANROOM_LLM_TIMEOUT:-180}"

MODEL="openai/gpt-5.1"
MODELDIR="openai_gpt-5_1"
MAX_PARALLEL="${MAX_PARALLEL:-3}"   # concurrent cells; override via env
RETRY_WAIT=120
MAX_ATTEMPTS=5

run_cell () {
  local srs="$1" lang="$2" stack="$3"
  local stem; stem="$(basename "$srs" .xml)"
  local out="outputs/matrix/${lang}/${stem}/${MODELDIR}"
  mkdir -p "$out"
  local attempt rc=1
  for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
    echo "[gpt51] START ${stem} | ${lang}/${stack} | attempt ${attempt}/${MAX_ATTEMPTS}"
    uv run python run_pipeline.py "$srs" \
        --language "$lang" --stack "$stack" --model "$MODEL" \
        --prove --certify --samples 1 --resume \
        --output-dir "$out" > "${out}/run.log" 2>&1
    rc=$?
    echo "[gpt51] DONE  ${stem} | ${lang} | attempt ${attempt} exit=${rc}"
    [ "$rc" -eq 0 ] && break
    [ "$attempt" -lt "$MAX_ATTEMPTS" ] && { echo "[gpt51] ${stem}/${lang} failed; ${RETRY_WAIT}s then resume…"; sleep "$RETRY_WAIT"; }
  done
}

throttle () {  # block until fewer than MAX_PARALLEL background cells are running
  while [ "$(jobs -rp | wc -l | tr -d ' ')" -ge "$MAX_PARALLEL" ]; do sleep 5; done
}

for SRS in \
    "data/srs/G16-SRS.xml" \
    "data/srs/SRS (Software Requirement Specification).xml" \
    "data/srs/Shoten_SRS.xml"; do
  for combo in "python:auto" "java:spring" "javascript:express"; do
    throttle
    run_cell "$SRS" "${combo%%:*}" "${combo##*:}" &
    sleep 3   # small stagger so cells don't all hit spec at the same instant
  done
done
wait
echo "[gpt51] all 9 cells finished — rebuilding CSV…"
uv run python scripts/collect_metrics.py --append --root outputs/matrix --out experiment_metrics.csv
echo "[gpt51] CSV updated. Done."
