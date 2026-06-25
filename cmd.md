# Run commands — Agentic Cleanroom

Every optional agent has its own ON/OFF switch, so an "arm" is just a flag combination over the
**same** harness, contracts (task spec), oracle, and metric code. Required agents — **Spec,
Planning, Code** — have no switch (the irreducible spec→code task given to every arm).

Pipeline: `SRS → [1]Spec → [2]Dependency → [3]Planning → [4a]Proof → [4]Code → [5]Test → [6]Certify → [6b]Recovery`

---

## Quick arms

```bash
# Full pipeline (proof + certify + recovery)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --prove --certify --samples 3

# Certify only, no recovery loop
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --no-recovery

# Minimal arm: spec → code only (no deps / proof / test / cert)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --no-dependency --no-test

# Baseline preset (== --no-prove --no-recovery --no-llm-deps --temperature 0)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --baseline --certify

# Generate + certify, plain (no proof)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --samples 1
```

---

## Ablation ladder (compare against the full pipeline)

Each row adds exactly one component, so the metric delta between rows attributes the gain.

```bash
# B0  raw: contract given, no proof, no recovery, no semantic deps
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --no-prove --no-recovery --no-llm-deps

# B1  + semantic dependency + clean-room
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --no-prove --no-recovery

# B2  + formal verification (prove-or-test)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --prove --no-recovery

# Full  + recovery loop
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --prove --max-cert-loops 2
```

---

## Per-agent switches

| Agent | Flag | Off behavior |
|---|---|---|
| Dependency | `--dependency` / `--no-dependency` | empty graph; features independent, spec order |
| Proof (Dafny) | `--prove` / `--no-prove` | proof tier skipped |
| Test | `--test` / `--no-test` | no test artifacts (cert, if on, synthesizes ephemeral tests) |
| Certify | `--certify` / `--no-certify` | no pass@k |
| Recovery | `--recovery` / `--no-recovery` | `== --max-cert-loops 0` |
| Semantic deps | `--llm-deps` / `--no-llm-deps` | regex-only FR edges (no LLM inference) |

Required (no switch): **Spec, Planning, Code**.

---

## Knobs

```bash
--language {python,java}        # target language (java → JUnit, stack fixed to java)
--stack {auto,python,fastapi}   # python sub-stack (ignored for java)
--samples N                     # code samples per FR for certification (default 1 = pass@1)
--k 1 3                         # pass@k values to report (default 1)
--max-cert-loops N              # recovery passes (default 2; 0 disables)
--prove-target {py,cs,js,go,java,cpp,rs}   # dafny translate target (default follows --language)
--prove-rounds N                # Dafny generate→verify→revise rounds per feature (default 6)
--temperature F                 # generation temp: spec/planning/code/test (default 0.0)
--cert-temperature F            # sampling temp for pass@k diversity (default 0.4)
--case-timeout F                # per-test-case execution timeout, seconds (default 10.0)
--output-dir PATH               # where to write artifacts (default outputs/)
```

### Per-stage model selection (each stage can run a different model; mixed cost priced accurately)

```bash
--spec-model        --dependency-model   --planning-model
--code-model        --test-model         --proof-model       --cert-model
# defaults: every stage gpt-4o-mini, proof gpt-4.1
```

Example — strong model only where it matters:

```bash
uv run python run_pipeline.py "data/srs/dineout_srs.xml" \
  --prove --certify --proof-model gpt-4.1 --code-model gpt-4o-mini
```

---

## Other SRS documents

```bash
uv run python run_pipeline.py "data/srs/2009 - video search.xml" --certify
uv run python run_pipeline.py "data/srs/gemini-code-1781976236207.xml" --certify
```

---

## Tests

```bash
uv run pytest -q                       # full suite
uv run pytest tests/test_recovery_loop.py -q
```

## Notes

- Needs `OPENAI_API_KEY` (or `OPENROUTER_API_KEY`) in `.env`. Set `OPENAI_BASE_URL` only for
  OpenRouter (and then models need an `openai/` prefix via `LLM_MODEL_PREFIX`).
- `--prove` needs a `dafny` binary on `PATH`/`$DAFNY`.
- Every run appends a row to `API_USAGE.md` and writes a report under `outputs/`.
