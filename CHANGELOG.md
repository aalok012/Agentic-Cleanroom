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

## 2026-06-20 — Deterministic CrossHair verification (python stack)

### Added
- **Step 1 — CrossHair symbolic verifier as a deterministic verdict source.** Why: the
  verification step should not depend on an LLM — CrossHair checks generated code against a
  spec-derived contract by symbolic execution (Z3), with no tests and no model in the loop.
  How: new [crosshair_verify.py](src/cleanroom/agents/verification/crosshair_verify.py) exposes
  `crosshair_verdicts(ir, code, only_fr_ids)` returning the same `ContractVerdict` shape as the
  executable verifier. For each `python`-stack FR it synthesizes a PEP 316 contract from the
  planning signature (a `post:` asserting the declared return type + `raises: ValueError` when
  `error_mode == 'raise'`), injects it into the function's docstring, and runs `crosshair check
  --analysis_kind=PEP316`. It reports two failure kinds: a return of the wrong type, and any
  UNDECLARED crash (KeyError/TypeError/IndexError/…) on some input.
- **Step 2 — Counterexamples abstracted to spec level (isolation-preserving).** Why: a CrossHair
  counterexample carries concrete failing inputs, which must never reach the Code Agent. How:
  `_abstract()` maps each counterexample to a `ContractViolation` describing only the violated
  property and failure kind (exception type / wrong return type), discarding the concrete
  argument values — so the revise loop stays spec-level like the LLM/executable verifiers.

### Changed
- **Step 3 — Wired CrossHair into both verify loops.** Why: every place code is generated and
  revised should get the symbolic check. How: [loop.py](src/cleanroom/agents/verification/loop.py)
  merges `crosshair_verdicts` via `merge_verdicts` in `generate_and_verify` (alongside the LLM +
  executable verdicts) and in `generate_with_executable_fixes` (the no-LLM deterministic path used
  by default for `--certify` on the python stack and by the CertificationAgent per-sample loop).
  `run_pipeline.py` prints whether CrossHair is active for the deterministic fix loop.
- **Step 4 — Gating + graceful degradation.** Why: CrossHair can only symbolically execute pure
  Python, and the solver may be missing. How: `crosshair_verdicts` returns `{}` on the `fastapi`
  stack (DB/HTTP code it cannot analyze) and when the `crosshair`/z3 tool is unavailable, so the
  pipeline never blocks on it. `_z3_env()` auto-discovers a libz3 matching the interpreter (e.g. a
  Homebrew build) when the bundled wheel's architecture differs.
- **Step 6 — Unified the two verify loops into one.** Why: after CrossHair, `generate_and_verify`
  and `generate_with_executable_fixes` shared the same deterministic core and revise loop, differing
  only by the LLM reviewer — duplicated logic that had to be edited twice (e.g. to add CrossHair).
  How: deleted `generate_with_executable_fixes`; `generate_and_verify(ir, code_agent, verifier=None,
  max_rounds=2)` now takes an optional `verifier` (`None` ⇒ token-free deterministic path:
  executable + crosshair only). Updated callers in `run_pipeline.py` and
  [evaluation/agent.py](src/cleanroom/agents/evaluation/agent.py) to call it with `verifier=None`
  and take `[0]`. No behavior change; full suite 35 passing.

### Dependencies
- **Step 5 — Added `crosshair-tool`** (`uv add crosshair-tool`), which pulls `z3-solver`. On this
  x86_64 (Rosetta) interpreter the bundled arm64 z3 wheel mismatches; the verifier falls back to
  the Homebrew x86_64 `libz3` at `/usr/local/opt/z3/lib` via `Z3_LIBRARY_PATH` auto-discovery.

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
- **Step 9 — Packager repairs the two most common FastAPI boot failures.** Why: the assembled
  DineOut app crashed at boot — `NameError: Integer` (Code Agent used a SQLAlchemy/FastAPI name
  it forgot to import) and `InvalidRequestError: Table 'orders' is already defined` (isolated FRs
  declare the same table under different class names). How: added `_ensure_known_imports` (adds/merges
  any referenced-but-unimported well-known fastapi/sqlalchemy/app symbol) and
  `_allow_table_redefinition` (injects `__table_args__ = {"extend_existing": True}` into each model
  declaring a `__tablename__`) to [packager.py](src/cleanroom/utils/packager.py); both are mechanical
  (imports/fixed attribute only, never logic), so isolation holds.
- **Step 10 — Fixed `_ensure_sqlalchemy_imports` NameError in the packager write loop.** Why: the
  build loop called the old name `_ensure_sqlalchemy_imports`, which no longer exists — every
  `build_runnable_package` (and the second boot test) crashed before writing a file. How: renamed
  the call to `_ensure_known_imports` at [packager.py](src/cleanroom/utils/packager.py).
- **Step 11 — FastAPI codegen now uses `Body(..., embed=True)` on every parameter.** Why: with a
  single plain `Body(...)` param FastAPI treats the whole request body as that value, so the HTTP
  oracle's dict-keyed POST (`{"param": value}`) returned 422 for single-parameter endpoints. How:
  changed both [generate_code.j2](src/cleanroom/agents/code/prompts/generate_code.j2) and
  [generate_code_revision.j2](src/cleanroom/agents/code/prompts/generate_code_revision.j2) to mandate
  `embed=True`, making the body `{"<param>": <value>, ...}` for any parameter count. Verified by a
  synthetic single-param endpoint returning `200` through `build_runnable_package` + `TestClient`.

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
