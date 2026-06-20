# Changelog

A step-by-step log of every change made to the Agentic Cleanroom project.
Newest entries go at the top. Each entry records **what** changed, **why**, and
**how** (the concrete files/commands), so the history is a readable audit trail.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/).
Categories used: `Added`, `Changed`, `Fixed`, `Removed`, `Docs`.

---

## How to read / add entries

Each dated section is one unit of work. Within it, list the individual steps in
the order they were performed:

```
## YYYY-MM-DD — short title

### Added | Changed | Fixed | Removed | Docs
- **Step 1 — <what>.** Why: <reason>. How: <files touched / command run>.
- **Step 2 — <what>.** ...
```

Keep each step small and concrete so anyone can follow the change after the fact.

---

## 2026-06-20 — Auto stack selection + FastAPI HTTP path + slimmer contract

### Removed
- **Step 1 — Dropped `current_state`, `new_state`, `state_invariant` from the behavioral contract.**
  Why: the state/invariant fields bloated the contract and the LLM filled them with vague
  prose that added little over precondition/postcondition. How: removed the fields from
  `BehavioralContract` and `FRContract` in
  [src/cleanroom/agents/spec_agent/schema/ir.py](src/cleanroom/agents/spec_agent/schema/ir.py),
  the matching bullets in [write_contract.j2](src/cleanroom/agents/spec_agent/prompts/write_contract.j2),
  both contract constructions in [spec_agent/agent.py](src/cleanroom/agents/spec_agent/agent.py),
  and the "State transition"/"Invariant" Notes blocks in `_compose_docstring`
  ([planning/agent.py](src/cleanroom/agents/planning/agent.py)). Updated `tests/test_planning_contracts.py`.

### Added
- **Step 2 — Deterministic target-stack classifier.** Why: stateless SRSs (video search) want
  pure functions; stateful CRUD SRSs (DineOut) need a real DB-backed web app — picking the
  wrong one produced fake in-memory state and hardcoded data. How: new
  [src/cleanroom/utils/stack_select.py](src/cleanroom/utils/stack_select.py) votes over
  spec-derived requirement text + preconditions and returns `(stack, reason)`. Verified:
  video search → python (29% stateful), DineOut → fastapi (80%).
- **Step 3 — `--stack auto` (now the default).** Why: select per SRS unless pinned. How:
  `run_pipeline.py` resolves the stack right after contract synthesis, stores `ir["stack"]`,
  and prints the decision; explicit `--stack python|fastapi` overrides.
- **Step 4 — FastAPI HTTP certification oracle.** Why: certifying web-stack code with the
  pure-function oracle was impossible (the original DineOut failure). How: `run_case_http` +
  `route_from_file_path` in [evaluation/runner.py](src/cleanroom/agents/evaluation/runner.py)
  assemble the runnable app and drive it via `TestClient` in a subprocess (200 JSON body for
  `eq`, 4xx for `raises`); `CertificationAgent` selects the oracle by stack and lays samples
  out via `build_runnable_package` for fastapi. New `tests/test_fastapi_oracle.py`.

### Changed
- **Step 5 — FastAPI codegen now emits real HTTP responses + errors.** Why: produce
  app-usable code with no hardcoding/fake state. How: the fastapi branch of
  [generate_code.j2](src/cleanroom/agents/code/prompts/generate_code.j2) (and the revision
  prompt) mandates DB-backed reads/writes, `@router.post("")` with `Body(...)` params,
  JSON return on success, and `HTTPException(4xx)` on failure; `_compose_docstring` emits
  `Raises: HTTPException` for the fastapi stack.

### Fixed
- **Step 6 — FastAPI/SQLAlchemy now installed (root cause #1).** Why: the cert subprocess
  raised `ModuleNotFoundError: fastapi`. How: `uv add fastapi sqlalchemy uvicorn httpx`.
- **Step 7 — Test Agent is now stack-aware (was emitting "vanilla" Python tests for FastAPI).**
  Why: the generated `pytest_source` imported routes flat and called them directly with
  `pytest.raises(ValueError)` — uncallable against the assembled FastAPI app. How: `TestAgent`
  takes `stack`; [generate_tests.j2](src/cleanroom/agents/test/prompts/generate_tests.j2) now
  emits a `TestClient` module that POSTs to the route and asserts `status_code`/`json()`
  (4xx for failures) on fastapi, plain function calls on python; threaded `stack` from
  run_pipeline stage 5 and the `CertificationAgent` fallback.
- **Step 8 — `requirement_for_prompt` now supplies the behavioral-contract fields.** Why: the
  test prompt referenced `r.stimulus`/`precondition`/`response`/`postcondition` and the route,
  none of which were provided — a latent `StrictUndefined` crash in the test stage. How: pulled
  them from `plan['contract']` and added a deterministic `route` (`route_for`) in
  [contracts.py](src/cleanroom/utils/contracts.py), mirroring `evaluation.runner.route_from_file_path`.

---

## 2026-06-16 — Remove stub LLM mode

### Removed
- **Step 1 — Deleted all stub LLM classes and flags.** Why: always running with real tokens;
  stubs added dead code and confusing `--stub-llm` / `--no-llm` CLI flags. How: removed
  `StubSpecLLM`, `StubDepLLM`, `StubPlanLLM`, `_PROMPT_REQ`, all hint/verb constants, and the
  `--stub-llm` / `--no-llm` args from `run_pipeline.py`. `run()` no longer takes `use_llm`,
  `spec_llm`, `plan_llm`, `dep_llm` params.
- **Step 2 — Simplified `main()`.** Why: clean entry point — just check for API key and run.
  How: `main()` now errors immediately if `OPENAI_API_KEY` is missing instead of silently
  falling back to stubs. `run()` signature is `(srs_path, output_dir, certify, samples)`.

---

## 2026-06-16 — Planning + Code Agent pipeline fixes

### Fixed
- **Step 1 — Always include Returns in docstrings.** Why: contracts with `-> None`
  signatures had no Returns section, making the docstring incomplete for the Code
  Agent. How: added `_infer_return_type(signature)` helper in
  [src/cleanroom/agents/planning/agent.py](src/cleanroom/agents/planning/agent.py);
  `_compose_docstring` now accepts the signature and falls back to inferring the
  return type annotation when the LLM returned an empty `returns` field.

- **Step 2 — Fixed `file_path` inconsistency between Planning and Code agents.**
  Why: `_file_path` was returning `outputs/{project}/code/models/func.py` (hardcoded
  prefix, pluralised layer) but `CodeAgent.write_files` was ignoring that path and
  reconstructing using the raw `mvc_layer` string (`model`, not `models`), so the
  path in the contract never matched the actual file on disk. How: changed
  `_file_path` in `planning/agent.py` to return a clean relative path
  `{layer_dir}/{func}.py` (e.g. `models/func.py`); changed `CodeAgent.write_files`
  in `code/agent.py` to use `output_dir / f.path` directly instead of
  reconstructing. Removed now-unused `project` variable from `plan()`.

### Verified
- **Step 3 — Confirmed Code Agent reads `planning.contracts`** (not the legacy
  `increment_plan`). The code at `code/agent.py:46` already does
  `(ir.get("planning") or {}).get("contracts")`. Updated the CHANGELOG baseline
  note below to reflect this.

---

## 2026-06-16 — Richer Google-style docstrings in Planning contracts

Goal: make each FR contract's docstring contain **summary + Args + Returns +
Constraints + Notes/Prerequisites** (Google style), instead of just a summary
with an NFR list. The LLM supplies the prose (summary, per-arg/return
descriptions); the section structure, NFR Constraints, and prerequisite Notes
stay deterministic.

### Changed
- **Step 1 — Extended the planner schema.** Why: the LLM now needs to return
  structured arg/return descriptions, not one flat string. How: in
  [src/cleanroom/agents/planning/schema/plan.py](src/cleanroom/agents/planning/schema/plan.py)
  added an `ArgDoc` model (`name`, `description`) and replaced `FRPlan.docstring`
  with `summary`, `args: list[ArgDoc]`, and `returns: str`. `Contract` is
  unchanged (still stores the final composed `docstring` string).
- **Step 2 — Updated the design prompt.** Why: tell the model to produce a
  summary, one `args` entry per signature parameter, and a `returns` phrase — and
  to NOT write Constraints/Notes itself (those are added deterministically). How:
  edited [src/cleanroom/agents/planning/prompts/plan_feature.j2](src/cleanroom/agents/planning/prompts/plan_feature.j2).
- **Step 3 — Rewrote `_compose_docstring`.** Why: assemble the Google-style
  docstring with `Args:` / `Returns:` / `Constraints:` / `Notes:` sections, each
  omitted when empty. How: in
  [src/cleanroom/agents/planning/agent.py](src/cleanroom/agents/planning/agent.py)
  rewrote `_compose_docstring(summary, args, returns, nfrs, prereq_notes)` and
  changed the NFR line format to `- <category>: <text>`.
- **Step 4 — Added deterministic prerequisite Notes.** Why: surface FR
  prerequisites in the docstring, referencing each by its designed function name +
  req id (e.g. `Prerequisite: create_lab_test_request (req 2.2.6.6) must have run
  first.`). How: new `_prereq_notes(prereq_ids, designs)` helper in `agent.py`,
  built from the inner `fr_edges`; wired into the `plan()` contract loop.
- **Step 5 — Updated the stub planner LLM.** Why: keep token-free `--stub-llm`
  runs working against the new `FRPlan` shape. How: `StubPlanLLM` in
  [run_pipeline.py](run_pipeline.py) now emits `summary` + `args` + `returns`.

### Verified
- **Step 6 — Ran the front pipeline token-free** (`uv run python run_pipeline.py
  "data/srs/2005 - phin.xml" --stub-llm`): completed, 0 tokens. Spot-checked the
  output `*_planning.json` — docstrings render all sections, including a
  `Prerequisite: ... (req X) must have run first.` Notes block (from `fr_edges`)
  and a `Constraints:` block (from a feature's NFRs).

## 2026-06-16 — Start the changelog

### Docs
- **Step 1 — Created `CHANGELOG.md`.** Why: to document every future change
  step by step in one clear, chronological place. How: added this file at the
  project root alongside `README.md`.
- **Step 2 — Recorded the current baseline (below)** so future entries have a
  reference point for what already existed before logging began.

### Baseline (state of the project when the changelog was started)
This is *not* a change — it is a snapshot of what already existed, summarized
from `README.md` and the existing code:

- **Front pipeline restructured and tested** (stages 1–3 wired in
  `run_pipeline.py`):
  - **[1] Spec** (`src/cleanroom/agents/spec_agent/`) — deterministic XML parse
    + per-feature FR/NFR classification.
  - **[2] Dependency** (`src/cleanroom/agents/dependency/`) — nested graph:
    deterministic outer feature DAG + inner per-FR graph, optional LLM semantic
    edges.
  - **[3] Planning** (`src/cleanroom/agents/planning/`) — one contract per FR
    (signature + docstring + MVC layer + file path + prerequisites).
- **Stages 4–6 exist and are wired** onto `planning.contracts` (`code/`, `test/`,
  `certification/`). `run_pipeline.py` runs them on real-LLM runs; stub runs stop
  after Planning.
- **Isolation guarantee** between Code and Test agents is enforced structurally.
