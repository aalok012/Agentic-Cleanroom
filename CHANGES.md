# Changelog

Session work on the Agentic Cleanroom pipeline (June 2026). Entries are ordered newest-first within each section.

---

## Last six changes (this session)

### 1. Executable certification (EvalPlus-style oracle)

- Replaced the **LLM judge** in stage 6 with a **subprocess runner** that executes structured test cases (`inputs_json` / `expected_json`).
- Added `src/cleanroom/agents/evaluation/runner.py`.
- Scoring unit is now **per FR** (HumanEval-style task), macro-averaged for aggregate pass@k.
- Reports **pass@1** and **pass@3** in `certification_report.md` and terminal output.

### 2. Planning + test I/O contract alignment

- Planning schema (`FRPlan` / `Contract`) gained:
  - `example_inputs_json`
  - `expected_return_json`
  - `failure_inputs_json` (empty when no failure test)
  - `error_mode` (`raise` | `return`)
- Test cases gained `inputs_json`, `expected_json`, `oracle` (`eq` | `raises`).
- Prompts require **JSON-serializable** signatures and **copy canonical I/O** from planning (no invented types or wrapper keys).

### 3. Default stack → plain Python for cert alignment

- `--stack python` is the default for code generation and certification.
- Code prompts enforce plain importable functions, `ValueError` on precondition violations, and exact canonical call/return behavior.
- **`--stack fastapi`** remains available for runnable HTTP packaging via `utils/packager.py`.

### 4. Prompt refinements for test/code agreement

- Documented **edit_order** semantics (positive quantity = target absolute qty; `-1` = remove dish).
- **assign_dishes_to_chefs**: must `raise ValueError` when no chef matches a classification.
- **mark_dish_as_cooked**: must `raise ValueError` when precondition violated.
- Test agent: **no failure case** when `failure_inputs_json` is empty (fixes spurious failures on zero-arg functions like `request_help()`).
- Verification: signature check ignores decorators / `Depends()` (underlying callable only).

### 5. Certification agent improvements

- `CertificationAgent` accepts `stack` and passes it to `CodeAgent` (fixes prior mismatch).
- **`use_pipeline_sample=True`**: sample 0 reuses stage-4 code; extra samples only when `--samples > 1`.
- Code sample temperature lowered to **0.4** for stabler certification.
- `failure_inputs_json` threaded through code generate/revise prompts.

### 6. Flask replaced with FastAPI (web packaging profile)

- Removed Flask from packager and prompts; added **FastAPI + SQLAlchemy** profile in `packager.py`, `plan_feature.j2`, `generate_code.j2`.
- FastAPI is for **deployment**; certification and tests target **`--stack python`**.

---

## Changes after DineOut SRS input (`data/srs/dineout_srs.xml`)

### SRS handling

- DineOut uses **`SystemRequirements` / `<Feature>`** XML (10 features, 1 FR each).
- Parser path: `build_system_requirements_features()` in `srs_reader.py` (same description text on feature + FR — not duplicate IDs).

### Initial DineOut runs (before alignment fixes)

| Setting | Result |
|---------|--------|
| Stack | `--stack fastapi` (default at the time) |
| Certification | LLM judge, `--samples 3` |
| **pass@3** | **0.700** |
| Case pass rate | **69.8%** (44/63) |
| Verification | **0/10** contracts passing after 1 revise round |

**Root causes identified:**

- Test agent expected **plain function calls**; FastAPI code used routes, `HTTPException`, custom types.
- Test/code **I/O shape mismatch** (dicts vs `DishSelection`, wrong return keys).
- Tests **invented** edge cases not in planning (e.g. invalid kwargs on `request_help()`).
- **edit_order** treated changes as deltas; planning expected absolute target quantities.

### DineOut runs (after python stack + executable cert + prompt refinements)

| Setting | Result |
|---------|--------|
| Command | `--stack python --verify --verify-rounds 1 --certify --samples 3` |
| Oracle | Executable subprocess |
| **pass@1** | **0.867** |
| **pass@3** | **0.900** |
| Case pass rate | **93.0%** (47/60) |

**FRs fixed:** 4.1, 4.2, 4.3, 4.4, 4.5 (previously failing or 0% pass@3).

**Remaining gaps (that run):** 4.6 (notification dict `complete: false` vs expected `true`), 4.7 (receipt string mismatch on one sample).

### Latest DineOut certification (in repo outputs)

From `outputs/generated/dineout_srs/certification_report.md`:

| Metric | Value |
|--------|-------|
| **pass@1** | **0.967** |
| **pass@3** | **1.000** |
| Case pass rate | **98.2%** |
| Weakest FR | 4.10 (pass@1 0.667; pass@3 1.000) |

### Recommended DineOut commands

```bash
# pass@1 only (fastest scored run)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" \
  --stack python --certify --samples 1

# pass@1 + pass@3 (default samples=3)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" \
  --stack python --verify --verify-rounds 1 --certify --samples 3

# All agents, minimum time
uv run python run_pipeline.py "data/srs/dineout_srs.xml" \
  --stack python --verify --verify-rounds 1 --certify --samples 1
```

---

## Files touched (summary)

| Area | Files |
|------|--------|
| Certification | `agents/evaluation/agent.py`, `runner.py`, `schema/certification.py`, `metric.py` |
| Planning | `agents/planning/schema/plan.py`, `agent.py`, `prompts/plan_feature.j2` |
| Code | `agents/code/agent.py`, `prompts/generate_code.j2`, `generate_code_revision.j2` |
| Test | `agents/test/schema/tests.py`, `prompts/generate_tests.j2`, `tools/spec_reader.py` |
| Verification | `agents/verification/prompts/verify_contract.j2` |
| Packaging | `utils/packager.py` (FastAPI) |
| Pipeline | `run_pipeline.py` |
| Docs | `README.md`, `CHANGES.md` |
