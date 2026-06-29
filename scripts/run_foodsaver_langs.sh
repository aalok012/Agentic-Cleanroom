#!/usr/bin/env bash
# Run foodsaver through ALL languages SEQUENTIALLY: python(fastapi) -> java(spring) ->
# javascript(express). Sequential (not concurrent) to avoid the half-delivered-JSON / connection
# failures concurrent deepseek/OpenRouter calls trigger. Every cell uses its own --output-dir and
# --resume, so a transient failure resumes from the failed stage instead of re-running the pipeline.
set -u
cd "$(dirname "$0")/.."

SRS="data/srs/foodsaver.xml"
COMMON=(--prove --certify --samples 1 --resume)

# More headroom against transient OpenRouter blips (these env vars are read by get_llm()).
export CLEANROOM_LLM_MAX_RETRIES="${CLEANROOM_LLM_MAX_RETRIES:-6}"
export CLEANROOM_LLM_TIMEOUT="${CLEANROOM_LLM_TIMEOUT:-180}"

run_cell () {
  local lang="$1"
  local stack="$2"
  local out="outputs/foodsaver_lang/${lang}"
  mkdir -p "$out"
  echo "[driver] === ${lang} (${stack}) -> ${out} ==="
  uv run python run_pipeline.py "$SRS" \
      --language "$lang" --stack "$stack" \
      "${COMMON[@]}" --output-dir "$out" \
      > "${out}/run.log" 2>&1
  echo "[driver] ${lang} exit=$?"
}

# python uses --stack fastapi explicitly (it auto-selected fastapi on the first run); its existing
# outputs/foodsaver_lang/python checkpoint — if any — lets --resume continue.
run_cell python fastapi
run_cell java spring
run_cell javascript express
echo "[driver] all languages complete."
