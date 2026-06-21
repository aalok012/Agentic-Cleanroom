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

## 2026-06-21 — LemmaFit/TypeScript stack: Phase 0 (discovery) + SPEC.yaml generator

Goal (user decision): move code generation from Python to a TypeScript stack verified by
**LemmaFit** (formal verification via Dafny, compiled to TS), replacing the CrossHair/executable
verification on that track.

### Changed (extended the Dafny syntax cheat-sheet — recovers syntax-failing features)
- **Added the Dafny forms the LLM kept getting wrong** to `DAFNY_REF` in both
  [dafny/agent.py](src/cleanroom/agents/dafny/agent.py) and
  [scripts/lemmafit_dafny_spike.py](scripts/lemmafit_dafny_spike.py): quantifiers/comprehensions use
  `|` for the range and `::` for the body (never `::` twice); functions are pure (no reassignment;
  `var x := e; <expr>` let-bindings only); every `if` needs an `else`; empty literals are `map[]` /
  `{}` / `[]` (not `set {}`/`map []`). Targeted spike re-runs (gpt-4.1) on the three syntax-failing
  features: **4.4 → VERIFIED** (5 rounds); **4.3** cleared its syntax error and advanced to the
  proof stage (7 verified, residual postcondition obligations); **4.6** cleared the syntax classes
  but then cascaded into deeper type/modeling errors — genuinely hard, like 4.10. So the cheat-sheet
  converts the simple syntax failures; the remaining failures (4.3 proof, 4.6 modeling, 4.10 proof)
  are real difficulty, not syntax. Expected full-run rate ≈ 7/10.

### Fixed (verification false-negatives — true rate is 6/10, not 4/10)
- **Dafny warnings were failing verified code.** `dafny verify`/`dafny translate` exit non-zero on
  STYLE warnings (e.g. `==>` indentation) even when every proof obligation is discharged. The verify
  adapter required `returncode == 0`, so it false-negatived two fully-verified DineOut features
  (4.7, 4.8). Fix: pass `--allow-warnings` and judge by the verification summary, not the exit code,
  in [dafny_verify.py](src/cleanroom/utils/dafny_verify.py); same `--allow-warnings` on the
  `dafny translate js` step in [lemmafit_project.py](src/cleanroom/utils/lemmafit_project.py).
  Corrected the DineOut run to its true result: **6/10 features verified** (4.1, 4.2, 4.5, 4.7, 4.8,
  4.9) and **6/6 compiled to runnable TS**. The 4 real failures are 3 Dafny **syntax** errors
  (4.3 closeparen, 4.4 else-branch, 4.6 set-comprehension — promptable) and 1 genuine **proof**
  failure (4.10, map-lookup precondition).

### Completed (Phases 1-6 — full LemmaFit/TypeScript pipeline, end to end)
- **`--stack lemmafit` wired through `run_pipeline`.** After Planning, a dedicated branch replaces
  the Python stages 4-6: scaffold a LemmaFit project, generate VERIFIED Dafny per feature, then
  compile to TypeScript. New constant `_DAFNY_MODEL = "gpt-4.1"` (the spikes proved weaker models
  can't discharge the proofs). `--stack` help updated.
- **Packager for the stack.** [lemmafit_project.py](src/cleanroom/utils/lemmafit_project.py):
  `scaffold_lemmafit_project` runs `lemmafit init` (lays down Replay.dfy + skills the DafnyAgent
  reads/verifies against); `compile_dafny_to_ts` appends a standard `AppCore` wrapper to each
  verified module and runs the bundled `dafny2js` to emit a TS client (best-effort). Fixed a
  path bug — dafny2js needs absolute paths when run with `cwd` set.
- **Certification = formal verification rate.** For this stack the Dafny proof IS the
  certification: `metrics['dafny']` reports verified/total + per-feature rounds; `--certify` adds
  the Dafny→TS compile stage. `write_run_report` gained Dafny-verification + TS-compile sections.
- **Runnable output completed.** The compile step now does LemmaFit's full 3-step chain so the
  output is genuinely runnable, not just an adapter: `dafny translate js` → copy to
  `src/dafny/<mod>.cjs` (the compiled verified logic) → `dafny2js --client` → `src/dafny/<mod>.ts`
  (typed adapter importing the .cjs). `scaffold_lemmafit_project` also runs `npm install`
  (best-effort) so a `--certify` run leaves a project you can `npm run dev` directly. Verified the
  4 DineOut features' `.cjs` load cleanly in Node.
- **End-to-end run (DineOut, `--stack lemmafit --certify`, gpt-4.1):** ran the full pipeline —
  **4/10 features formally verified** (4.1, 4.2, 4.5, 4.9) and **4/4 verified → compiled to
  TypeScript** clients via dafny2js; 276k tokens, $0.81, auto-logged to API_USAGE.md (gpt-4.1
  priced correctly). The mutating features that fail (4.3/4.4/4.6/4.7/4.8/4.10) need more
  proof-tactic scaffolding or rounds — the known map-comprehension proof difficulty.

### Added (Phase 3 — Dafny agent + token logging)
- **Stage-3 `DafnyAgent`.** Productionizes the validated spike into a reusable agent:
  [dafny/agent.py](src/cleanroom/agents/dafny/agent.py) `DafnyAgent.generate(ir)` casts each feature's
  FRs into a Dafny `Domain` state machine (one `Action` per FR; BehavioralContract → Inv / guards /
  postcondition lemmas) and runs the generate→`verify_dafny`→revise loop (system prompt = LemmaFit's
  shipped skills + abstract Domain interface + Dafny syntax cheat-sheet; default gpt-4.1). Spec-derived
  only (never reads tests). Schema [dafny/schema/dafny.py](src/cleanroom/agents/dafny/schema/dafny.py).
  Offline tests (fake LLM + real Dafny verifier) [tests/test_dafny_agent.py](tests/test_dafny_agent.py):
  verifies round 1; revises to round 2; reports unverified after budget. Full suite 47 passing.
- **Token logging.** Instrumented `scripts/lemmafit_dafny_spike.py` to auto-append usage to
  API_USAGE.md; added gpt-4o/gpt-4.1 prices + prefix matching to
  [cost.py](src/cleanroom/utils/cost.py); logged the five earlier spikes as `spike-estimate` rows
  (~100k tokens; cost caveat noted in API_USAGE.md).

### Discovery (Phase 0)
- **Installed and inspected LemmaFit** (`npm install -g lemmafit`; `lemmafit init`). Findings that
  shape the build: it is a **Dafny Replay/Redux state machine** (`type Model`, `datatype Action`,
  `predicate Inv`, `Init`/`Apply`/`Normalize`, lemmas `InitSatisfiesInv`/`StepPreservesInv`),
  driven **SPEC.yaml-first** (structured entries: id/req_id/title/group/layer/type/property/module/
  verifiable/guarantee_type/state), compiled to a TS API via `lemmafit add <Name> --target ...`, and
  verified by a daemon. React+TypeScript **greenfield only**, **effect-free only**, Claude-Code-
  oriented. Implication: each FR becomes an `Action`; the BehavioralContract maps to SPEC.yaml
  (precondition→precondition entry, response/postcondition→postcondition entry + ensures lemma).

### Verified (Stage-3 LLM feasibility spike)
- **An LLM can author verifying Dafny via the verify-loop — with a capable model.** Built
  [scripts/lemmafit_dafny_spike.py](scripts/lemmafit_dafny_spike.py): seeds the model with
  LemmaFit's shipped skills + the abstract `Domain` interface, generates a state machine for one
  feature from its spec contracts only (cleanroom), runs `verify_dafny`, and feeds proof errors
  back ≤5 rounds. Results on DineOut FR 4.1: **gpt-4o-mini FAILED** (stuck on a Dafny syntax error,
  0 rounds of progress — too weak); **gpt-4o VERIFIED in 4 rounds** (errors shrank 1→1→1→0 as it
  used the real Dafny feedback). Conclusion: the TypeScript/LemmaFit track is feasible but
  **requires a strong model (gpt-4o class)** — the pipeline's gpt-4o-mini default cannot author
  Dafny. (Caveat: FR 4.1 is a read-only action so its `Apply` is trivial; a mutating feature is the
  next, harder signal.)
- **Mutating-feature spike (FR 4.10 manage-menu, gpt-4o) — graded result.** First run looped on a
  Dafny map-syntax parse error (`gets expected`); adding a **Dafny syntax cheat-sheet** to the prompt
  (map update `m[k:=v]`, removal `m-{k}`, comprehension `map k | k in m && P :: m[k]`, datatype
  records) **fixed all syntax errors** → `5 verified`. But it then stalled on **proof** obligations
  (`function precondition could not be proved` ×8, oscillating across 6 rounds): proving how a
  map-comprehension `Normalize` interacts with map updates needs helper lemmas gpt-4o doesn't write.
  Conclusion: feasibility is **graded by feature complexity** — read-only/simple `Apply` verifies;
  **mutating + map-state features exceed gpt-4o within 6 rounds** and need a stronger reasoning model,
  proof-tactic/helper-lemma scaffolding in the prompt, or an `assumed`-axiom fallback. Syntax issues
  are promptable; map-comprehension proofs are the real wall.
- **Same mutating feature with gpt-4.1 — VERIFIED in 2 rounds.** The proof wall is a model-capability
  issue: gpt-4.1 authored a genuine CRUD state machine for FR 4.10 (`Model = map<string, MenuItem>`,
  Add/Edit/Delete actions with real map updates, an invariant tying keys to item names + non-negative
  prices, a map-comprehension `Normalize`, and a **biconditional postcondition lemma**
  `AddItem_Postcondition`) that Dafny accepts. Verdict for the LemmaFit/TS pivot: **feasible end to
  end with gpt-4.1** — the chain (LemmaFit skills + Domain interface + Dafny syntax cheat-sheet +
  `verify_dafny` revise loop) produces verifying Dafny for both read-only and mutating CRUD features.
  Model requirement is firm: gpt-4o-mini (pipeline default) and gpt-4o are insufficient for mutating
  features; **Stage 3 needs gpt-4.1-class**.

### Added
- **Feasibility spike + Dafny verify adapter (Phase 1/4 de-risk, token-free).** Why: the whole
  pivot hinges on producing Dafny that actually verifies — validate that before building the LLM
  agent. How: scaffolded a real project (`lemmafit init outputs/lemmafit_dineout` + `npm install`,
  which downloads Dafny 4.11 to `~/.lemmafit/.dafny`); confirmed synchronous verification works;
  **hand-authored `PlaceOrder.dfy`** mapping DineOut FR 4.1 to a state machine (`Model`/`Action`/
  `Apply`/`Inv` + `InitSatisfiesInv`/`StepPreservesInv` + a domain postcondition lemma
  `AddDishGrowsOrder`) — **verifies, 10 verified / 0 errors**. Built the reusable Stage-4 core
  [dafny_verify.py](src/cleanroom/utils/dafny_verify.py) (`verify_dafny()` locates the binary, runs
  `dafny verify`, parses pass/fail + error locations to feed the revise loop). Tests:
  [tests/test_dafny_verify.py](tests/test_dafny_verify.py). Confirms the FR→Action→Apply→ensures-lemma
  mapping yields verifiable Dafny; the open risk is now only whether the LLM can author it (Stage 3).
- **SPEC.yaml generator (Phase 1 start).** Why: LemmaFit's first step is SPEC.yaml; our spec stage
  already extracts the needed pre/post/response per FR. How: new
  [lemmafit_spec.py](src/cleanroom/utils/lemmafit_spec.py) `build_spec_yaml(ir)` /
  `build_spec_entries(ir)` emit one `precondition` + one `postcondition` entry per FR (postcondition
  falls back to the response), with a per-feature Dafny `module` name, `depends_on` linked from
  prerequisite FRs, and `state: DRAFT` (the Dafny stage formalizes `property` and flips to
  ADDRESSED). Deterministic, spec-derived (never reads tests/code) → isolation holds. Tests:
  [tests/test_lemmafit_spec.py](tests/test_lemmafit_spec.py). Full suite 42 passing.

## 2026-06-21 — Pin the entity identifier in the contract (Code/Test agree on the key)

### Added
- **Step 1 — `entity_identifier` on the planning contract.** Why: with the two-phase oracle, the
  Test Agent seeded staff by `name` while the Code Agent looked them up by `id`, so edit/delete
  still failed ("ID required" / "not found") — the contract never pinned the entity's key, so the
  two agents diverged (same family as the 4.4 type mismatch). How: added `entity_identifier` to
  `FRPlan` and `Contract` ([planning/schema/plan.py](src/cleanroom/agents/planning/schema/plan.py)):
  the single field that uniquely keys a persisted entity for lookup (e.g. `id`/`name`), empty for
  stateless FRs. The planner LLM produces it
  ([plan_feature.j2](src/cleanroom/agents/planning/prompts/plan_feature.j2) — "pick a key the
  stimulus actually provides on edit/delete"); the agent threads it into every `Contract`.

### Changed
- **Step 2 — Both agents key off it.** Why: code and tests must use the same field. How: the Code
  Agent passes `entity_identifier` into [generate_code.j2](src/cleanroom/agents/code/prompts/generate_code.j2)
  and the revision prompt (fastapi: "look up/store the entity by its `<field>`; don't require an
  identifier the caller doesn't send"); `requirement_for_prompt`
  ([contracts.py](src/cleanroom/utils/contracts.py)) surfaces it to
  [generate_tests.j2](src/cleanroom/agents/test/prompts/generate_tests.j2), whose SETUP rule now
  says the seed call and the main call MUST share the same identifier value. Template tests updated;
  full suite 38 passing.

## 2026-06-21 — Fix FastAPI boot crash: unify same-table models

### Fixed
- **Step 1 — Collapse differently-named models that map to the same table.** Why: a regenerated
  DineOut run crashed every case at boot with `ArgumentError: Trying to redefine primary-key column
  'name' as a non-primary-key column` (pass@1 0.2 → 0.0). Two isolated FRs modeled the `dishes`
  table incompatibly — `DishModel(id PK, name, quantity)` vs `Dish(name PK, classification)` — and
  `extend_existing=True` tried to merge them. `_dedupe_models` only collapses same-CLASS-NAME
  redefinitions, so this slipped through. How: new `_unify_models_by_table` in
  [packager.py](src/cleanroom/utils/packager.py) picks one canonical class per table (prefer the
  `models` layer, then the richest definition), gives it the UNION of all columns with a single
  primary key (`id` if any def has one, else the first declared PK; others demoted), and rewrites
  every other same-table class into an import alias of the canonical. Wired in after
  `_dedupe_models`. Re-certifying the existing code: boot restored, case rate 0.0 → **0.625**.
  Regression test: [tests/test_packager_models.py](tests/test_packager_models.py). Full suite 38 passing.

## 2026-06-20 — Two-phase (seed-then-act) FastAPI certification oracle

### Added
- **Step 1 — Spec-level `setup` on each test case.** Why: the FastAPI cert oracle did a single
  POST against a freshly-created EMPTY database, so stateful happy-paths (edit/delete/cancel/read an
  existing entity) were unpassable and error-cases passed spuriously (everything 404'd before the
  real check ran). How: added `setup_json` to `TestCase`
  ([test/schema/tests.py](src/cleanroom/agents/test/schema/tests.py)) — a JSON array of Arrange
  calls, each `{"inputs": <body>, "route"?: <route>}`, that create the precondition state through
  the API. It is spec-level (API calls with spec-derived inputs), so the cleanroom holds — no table
  or column names ever appear.
- **Step 2 — Two-phase HTTP oracle.** Why: replay the Arrange calls before the Act call against the
  same persistent sqlite file. How: `_HTTP_RUNNER_SCRIPT`/`run_case_http`
  ([evaluation/runner.py](src/cleanroom/agents/evaluation/runner.py)) take a 6th `setup_json` arg,
  POST each setup step in order (default route = the FR's own endpoint), and fail the case at Arrange
  if any setup step returns ≥400; then do the Act POST and assert as before. Verified on the REAL
  generated `manage_staff_records`: "edit existing staff" goes 404→pass, and "delete missing id"
  now 404s for the right reason (data exists, id absent) instead of spuriously.

### Changed
- **Step 3 — Test Agent emits setup.** Why: the agent (spec-only) must declare the Arrange calls.
  How: [generate_tests.j2](src/cleanroom/agents/test/prompts/generate_tests.j2) instructs (fastapi
  only) to populate `setup_json` with create/add calls using the SAME identifiers the main inputs
  reference, to leave it empty for pure-create / state-as-input cases, and to NOT seed an entity a
  "not found" case looks up; the fastapi `pytest_source` replays setup before the main POST.

### Tests
- **Step 4 — Two-phase oracle tests.** New cases in
  [tests/test_fastapi_oracle.py](tests/test_fastapi_oracle.py): a CRUD endpoint's stateful happy-path
  fails without setup and passes with it, and a failing Arrange step is reported as `setup step 0`.
  Full suite 37 passing.

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
