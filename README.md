# Agentic Cleanroom

A multi-agent pipeline that turns a **Software Requirements Specification (SRS)** into a working
application, and then **certifies each feature one of two ways**:

- **PROVED** — the feature's logic is written in [Dafny](https://dafny.org/), **formally verified**
  (`dafny verify`), and compiled to native code. Correct by construction.
- **TESTED** — for features that can't be proved (or whose logic is effectful), the code is generated
  normally and scored with **pass@k** against spec-derived black-box tests.

The non-negotiable rule throughout is **clean-room isolation**: the code generator never sees the
tests, and the test generator never sees the code. They agree only by anchoring to the same
specification. That's what makes pass@k an honest measurement instead of a number you can game by
feeding failing tests back into the generator.

> **Status, in one line:** the full pipeline runs end-to-end. On the DineOut SRS a real run proves
> 6/10 features in Dafny and tests the other 4. The Dafny proof track and the FastAPI adapter that
> ships proved logic are the newest parts and have the sharpest edges — see
> [Status & known limitations](#status--known-limitations).

---

## The core idea

In a typical "agentic coding" setup, failing tests are fed back into the code generator until they
pass — so the code overfits to the tests and the score means little. Here the two sides are kept
apart by construction:

- **Code** is a pure function of the **specification** (plus, optionally, *spec-level* contract
  violations from an independent reviewer — never test data).
- **Tests** are a pure function of the **specification**.
- They meet exactly once, at **certification**, and only **after both are frozen**. Certification
  scores; it never writes back into generation.

On top of that, the pipeline adds a **formal verification track**. Where a feature's logic can be
expressed as a pure state machine, it is authored in Dafny and *proved* rather than tested. Proof is
a stronger guarantee than any number of passing tests — but Dafny is **effect-free**, so it can only
cover pure logic, not databases or HTTP. That boundary shapes the whole design.

---

## Pipeline overview

`run_pipeline.py` is plain sequential Python — no graph framework. Each stage reads and extends a
shared **Intermediate Representation (IR)**, a JSON document that accumulates artifacts as the run
progresses (`outputs/{project}_full_ir.json` is the complete record).

```
  SRS.xml
    │
    ▼
  [1] Spec Agent        parse functional requirements (deterministic) + behavioral contracts (LLM)
    │                   → auto-select the app stack: python (pure functions) or fastapi (DB-backed)
    ▼
  [2] Dependency Agent  nested dependency graph + build order (regex, optional LLM for FR→FR edges)
    │
    ▼
  [3] Planning Agent    one implementation contract per FR (signature, mvc_layer, file path, prereqs)
    │
    ▼
  [4a] Proof tier       (optional, --prove) author + PROVE each feature in Dafny, compile proved
    │                   features to native code (gpt-4.1 + the dafny binary)
    ▼
  [4]  Code Agent       PROVED features → a thin FastAPI adapter over the compiled Dafny core
    │                   UN-proved features → full generated code
    ▼  (optional, --verify)
  [4b] Verification     reasoning-only contract review + bounded revise loop (LLM, no execution)
    │
    ▼
  [5] Test Agent        spec-derived black-box test cases (LLM)
    │
    ▼  (optional, --certify)
  [6] Certification     pass@k via an executable/HTTP oracle — for UN-proved features only
```

The proof tier (4a) runs **before** code generation so the Code Agent knows which features ship
from Dafny. The full prove-or-test flow is `--prove --certify`.

| Stage | LLM? | Adds to IR |
|-------|------|------------|
| 1 Spec | parse: no · contracts: yes (1 call/feature) | `features`, `contracts`, `stack` |
| 2 Dependency | regex: no · FR edges: optional LLM | `dependency_graph`, per-feature `fr_*` |
| 3 Planning | yes (1 call/feature) | `planning.contracts` |
| 4a Proof tier | **gpt-4.1** (1+ calls/feature, opt-in `--prove`) | `generated_dafny`, `proved_feature_ids` |
| 4 Code | yes (1 call/FR or adapter) | `generated_code` |
| 4b Verification | yes (opt-in `--verify`) | `verification` |
| 5 Test | yes (1 call/feature) | `generated_tests` |
| 6 Certification | executable oracle (opt-in `--certify`) | `certification` |

---

## The two certification tiers

This is the heart of the project. Every feature exits a `--prove --certify` run with exactly one
honest label.

### PROVED — formal verification (Dafny)

1. The **Dafny Agent** (`agents/dafny/`) casts a feature's functional requirements into a Dafny
   state machine that refines a vendored **Replay/Redux kernel** (`agents/dafny/kernel/Replay.dfy`):
   `type Model`, `datatype Action` (one variant per FR), `predicate Inv`, `Init` / `Apply` /
   `Normalize`, and the proof obligations `InitSatisfiesInv` / `StepPreservesInv`.
2. It runs a **generate → `dafny verify` → revise** loop (default 6 rounds). The model is **gpt-4.1**
   — weaker models can't discharge the proofs (gpt-4o-mini can't even parse Dafny).
3. A feature is **proved** when `dafny verify` reports `0 errors`. It is then compiled to native
   code with `dafny translate <target>` (default Python).
4. On the FastAPI stack, the Code Agent writes only a **thin adapter** over the compiled core
   (HTTP route + DB persistence + marshalling) — it does **not** rewrite the logic. The business
   logic that ships is the proved Dafny.

"Verified" means the state machine can never reach a state violating its invariant. The proof
covers the *compiled* logic, not a parallel sketch — the verified Dafny is the source that compiles
into what runs.

An unprovable obligation can pass via an explicit, auditable `assume {:axiom}` escape hatch; such a
feature is labelled `PROVED [N assumed axiom(s)]` so assumptions are never silent.

### TESTED — pass@k

Features the proof tier can't verify (a genuine proof wall, or inherently effectful logic) fall back
to the normal path: the Code Agent generates the full implementation, and the **Certification Agent**
scores it with **pass@k** against the Test Agent's spec-derived tests. Proved features are excluded
from pass@k (proof is their certification).

### Why both?

Dafny is **effect-free** — it proves validation, state transitions, and computations, but not DB
writes, HTTP, or I/O. So a DB-backed app is only *partially* provable: the model-layer logic can be
proved; the controllers/persistence always go through the test track. Prove-or-test makes that
boundary explicit instead of pretending one tool covers everything.

---

## Running it

### Setup

**Prerequisites:** [uv](https://docs.astral.sh/uv/), Python ≥ 3.11, an OpenAI API key, and — for the
proof tier only — a `dafny` binary on `PATH`.

```bash
uv sync
echo "OPENAI_API_KEY=sk-..." > .env
brew install dafny            # only needed for --prove (Dafny 4.11)
```

Default model is **gpt-4o-mini** (`src/cleanroom/utils/llm_client.py`); the proof tier overrides to
**gpt-4.1**.

### Commands

```bash
# 1. Basic: spec → code → tests (no scoring)
uv run python run_pipeline.py "data/srs/dineout_srs.xml"

# 2. Test track only: pass@k certification
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --certify --samples 3

# 3. The full prove-or-test flow (needs dafny + gpt-4.1; spends ~$0.6 on DineOut)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --stack fastapi --prove --certify --samples 1

# 4. LLM contract review + revise loop (independent of prove/test)
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --verify --verify-rounds 2
```

### Flags

| Flag | Default | Meaning |
|------|---------|---------|
| `--stack` | `auto` | App stack: `auto` (chosen from the spec), `python`, or `fastapi` |
| `--prove` | off | Run the Dafny proof tier; proved features compile to native code (needs `dafny` + gpt-4.1) |
| `--prove-target` | `py` | `dafny translate` target for proved features (`py`/`cs`/`js`/`go`/`java`/`cpp`/`rs`) |
| `--certify` | off | Run pass@k certification (for the un-proved features when `--prove` is on) |
| `--samples` | 3 | Code samples per FR for pass@k |
| `--verify` | off | LLM contract reviewer + bounded revise loop after code generation |
| `--verify-rounds` | 2 | Max revise rounds (`0` = review only) |
| `--verify-model` | gpt-4o-mini | Model for the reviewer |
| `--verify-passes` | 1 | Reviewer passes per contract; `>1` requires a unanimous fail before revising |
| `--output-dir` | `outputs` | Artifact directory |

### Re-score for free (no re-proving)

`scripts/recertify.py` re-runs certification against an existing finished run, reusing its proved
artifacts. `n=1` makes **zero LLM calls**; `n>1` generates the extra samples with gpt-4o-mini.

```bash
uv run python scripts/recertify.py outputs/dineout_srs_full_ir.json      # free, n=1
uv run python scripts/recertify.py outputs/dineout_srs_full_ir.json 4    # pass@4
```

---

## The agents

Each agent lives under `src/cleanroom/agents/<name>/` with `agent.py`, a `schema/`, and (where an
LLM is used) `prompts/*.j2`.

**1. Spec Agent** (`spec_agent/`) — deterministically parses the SRS into features +
functional-requirement IDs (narrative/non-functional sections are ignored), then makes one LLM call
per feature to write a **behavioral contract** per FR (stimulus / precondition / response /
postcondition). IDs come from the parser; the LLM never invents them. Supports both the legacy
`req_document` format and the `<Feature>` format (e.g. DineOut). After contracts exist, a
deterministic keyword vote picks the stack (`python` vs `fastapi`).

**2. Dependency Agent** (`dependency/`) — builds a nested dependency graph: an outer
feature-level DAG and inner FR→FR edges, with a `build_order` and cycle detection. Informational
cross-references ("more information found in section X") are filtered out so they don't create fake
prerequisites — this is what fixed an early phantom 2.2↔2.5 cycle.

**3. Planning Agent** (`planning/`) — attaches implementation metadata to each contract:
`signature` and `mvc_layer` (LLM), and `docstring` / `file_path` / `prerequisite_fr_ids`
(deterministic). For `--stack fastapi`, signatures are shaped as route handlers / model functions.

**4a. Dafny Agent** (`dafny/`) — the proof track. Authors a Dafny state machine per feature from the
spec, verifies it with `dafny verify` (`utils/dafny_verify.py`), and revises on proof errors. The
prompt carries an owned Dafny **syntax cheat-sheet** (`DAFNY_REF`) and **proof tactics** (`PROOF_REF`).
Compiles proved features via `utils/dafny_project.py` (`compile_dafny`).

**4. Code Agent** (`code/`) — generates one source file per planning contract
(`generate(ir, skip_feature_ids=…)`), or, for a proved feature on FastAPI, a thin adapter over the
compiled core (`generate_adapter`, prompt `generate_adapter.j2`). The adapter imports the compiled
Dafny module + the marshalling shim (`utils/dafny_marshal.py`), persists the Dafny `Model` as state,
and calls `Normalize(Apply(state, action))`. Structurally cannot read tests; the only feedback
channel is `revise()` from the Verification Agent's spec-level violations.

**4b. Verification Agent** (`verification/`) — an independent, **reasoning-only** reviewer (no
execution) that checks a generated file against its contract and returns clause-level violations
(precondition / response / postcondition / …). The bounded `generate_and_verify` loop in `loop.py`
revises failing files and re-verifies. (This is now the *only* verifier on the code side — the
earlier deterministic layers, CrossHair and an executable oracle, were removed; deterministic
verification moved entirely to the Dafny track.)

**5. Test Agent** (`test/`) — derives black-box test cases from the spec only (features + contracts +
planned signatures), one call per feature. Writes `test_feature_*.py`. Never reads generated code.

**6. Certification Agent** (`evaluation/`) — pass@k (Chen et al.). An **executable oracle** runs each
test case in a subprocess (a direct function call for `python`, an HTTP call via `TestClient` for
`fastapi`, with two-phase Arrange/Act seeding). A sample passes an FR only if **all** its cases pass;
results are macro-averaged over FRs. Skips features already proved by the Dafny tier.

---

## Clean-room isolation

```
                        ┌─────────────┐
                        │     SPEC    │
                        │ (SRS + IR)  │
                        └──────┬──────┘
        ┌──────────────┬───────┼───────┬──────────────┐
        ▼              ▼       ▼       ▼              ▼
   Dafny Agent    Code Agent  Test   Verification   (stack select)
   (spec only)    (spec only) Agent  (spec + code under review,
        │              │      (spec   spec-level feedback only)
   proved core    full code    only)
        └──────┬───────┘         │
               ▼                 │
         Certification ◄─────────┘
       (executable oracle, no feedback to generation)
```

| Agent | May read | Must never read |
|-------|----------|-----------------|
| Dafny | spec, planning contracts | tests, generated code |
| Code | spec, planning contracts, the proved Dafny it wraps, contract violations | `generated_tests` |
| Test | features, contracts, planning | `generated_code` |
| Verification | spec, planning, the code under review | `generated_tests`; no execution |
| Certification | frozen tests + code samples | (scores only; never writes back) |

---

## Outputs

After a run:

| Path | Description |
|------|-------------|
| `outputs/{project}_full_ir.json` | Complete enriched IR + metrics (the audit trail) |
| `outputs/{project}_run_report.md` | Per-stage timing/tokens/cost, proof ledger, pass@k |
| `outputs/generated/{project}/app/` | Runnable FastAPI app (`--stack fastapi`) |
| `outputs/generated/{project}/app/dafny_cores/` | Compiled proved cores + the marshalling shim |
| `outputs/generated/{project}/dafny_proof/dafny/*.dfy` | Generated Dafny per feature (`--prove`) |
| `outputs/generated/{project}/dafny_proof/out/F…-py/` | Compiled proved logic |
| `outputs/generated/{project}/tests/` | Pytest modules (`test_feature_*.py`) |
| `API_USAGE.md` | Append-only token/cost ledger — written on **every** run, success or failure |

**Cost accounting is per-model.** A `--prove` run mixes gpt-4.1 (proof) and gpt-4o-mini (everything
else); `API_USAGE.md` prices each model's tokens at its own rate (e.g. the DineOut run logged
`$0.6249`, model `gpt-4.1+gpt-4o-mini`), not all tokens at one rate.

---

## Example results (DineOut SRS, FastAPI, `--prove --certify`)

```
Proof tier:  6/10 features PROVED   → 4.1, 4.2, 4.4, 4.5, 4.8, 4.9   (compiled to Python)
Test track:  4/10 features TESTED   → 4.3, 4.6, 4.7, 4.10
             4.3  pass@1 1.00 (4/4)
             4.10 / 4.6 / 4.7  fail several cases
             aggregate pass@1 ≈ 0.25, case-rate ≈ 0.60
Cost: ~$0.62 (logged, mixed-model)
```

The four un-proved features hit two kinds of wall: **syntax/proof** in Dafny (e.g. 4.10's
map-comprehension postcondition, 4.6's malformed `ensures`) and, on the test side, **missing setup
steps** — the Test Agent currently writes "edit an *existing* item" cases without first creating the
item, so they hit an empty DB. Both are documented below.

---

## Status & known limitations

This is a research/engineering pipeline. Being explicit about what's solid and what isn't:

- **Proved features compile and import, but their adapter *routes* aren't independently asserted.**
  Proof is their certification and pass@k skips them, so route-level behavior of the thin glue is
  not separately checked.
- **Dafny adapter quality is the youngest part.** The first real run surfaced two bugs that offline
  tests missed: the certification oracle didn't stage the compiled cores into its sample apps (every
  test failed at boot), and Dafny mangles `_`→`__` in compiled module names (`F4_1Domain` →
  `F4__1Domain`). Both are fixed and regression-tested, but expect more such edges on new SRSs.
- **Proof walls are real.** Map-lookup preconditions and map-comprehension postconditions need
  helper lemmas the model doesn't always produce in budget. More *rounds* don't help once the error
  plateaus — better proof-tactic hints or the `assume {:axiom}` hatch do.
- **The test track can be unfair.** Stateful "edit/delete/mark an existing X" cases are generated
  without Arrange/seed steps, so they fail against an empty DB even when the code is correct. The
  two-phase oracle supports seeding; the Test Agent doesn't yet emit the seed calls.
- **`dafny translate py` output is runtime-flavored**, not idiomatic Python — it's a verified library
  the adapter calls through `dafny_marshal`, not hand-editable code.
- The proof tier requires **gpt-4.1**; smaller models are insufficient.

---

## Project layout

```
agentic-cleanroom/
├── run_pipeline.py                     # End-to-end runner (stages 1–6)
├── scripts/recertify.py                # Free re-scoring against existing proved artifacts
├── data/srs/                           # Input SRS documents (XML)
├── outputs/                            # IR, reports, generated apps, compiled Dafny
├── API_USAGE.md  ·  CHANGELOG.md       # Token/cost ledger · step-by-step change log
└── src/cleanroom/
    ├── agents/
    │   ├── spec_agent/                 # [1] parse + behavioral contracts
    │   ├── dependency/                 # [2] nested dependency graph
    │   ├── planning/                   # [3] implementation contracts
    │   ├── dafny/                      # [4a] Dafny proof author
    │   │   ├── agent.py                #      generate→verify→revise (DAFNY_REF + PROOF_REF)
    │   │   └── kernel/Replay.dfy       #      vendored Redux/Replay kernel (no LemmaFit dep)
    │   ├── code/                       # [4]  full code + generate_adapter + generate_adapter.j2
    │   ├── verification/               # [4b] LLM contract reviewer + revise loop
    │   ├── test/                       # [5]  black-box tests
    │   └── evaluation/                 # [6]  pass@k certification (executable/HTTP oracle)
    ├── llms/callbacks/metric.py        # Per-call token/model tracking (all LLM calls)
    └── utils/
        ├── dafny_verify.py             # run `dafny verify`, parse result, extract axioms
        ├── dafny_project.py            # scaffold project, compile_dafny, stage_dafny_cores
        ├── dafny_marshal.py            # JSON/DB ↔ Dafny runtime types (shipped into the app)
        ├── dafny_spec.py               # IR contracts → SPEC.yaml entries
        ├── packager.py                 # FastAPI app assembly
        ├── stack_select.py             # deterministic python/fastapi choice
        └── cost.py                     # per-model cost (estimate_cost_by_model)
```

---

## Design principles

1. **Deterministic-first.** IDs, parsing, grouping, ordering, file paths, and docstrings are plain
   code. The LLM is used only for interpretation (contracts, signatures, code, Dafny, tests, review).
2. **The LLM never owns IDs.** Requirement IDs come from the parser; unrecognized IDs are dropped.
3. **Structured output.** Schemas live in Python (`with_structured_output`), not in prompts.
4. **Token discipline.** One LLM call per unit of work; agents get only the scoped slice they need.
5. **The IR is the audit trail.** Every stage appends keys; `{project}_full_ir.json` is the record.
6. **Structural isolation.** Code and tests cannot see each other's artifacts by construction;
   verification feedback is spec-level only; certification scores without writing back.
7. **Prove what you can, test the rest — and label it honestly.** No tier pretends to a guarantee it
   doesn't have.

Project change history is in **[CHANGELOG.md](CHANGELOG.md)** (step-by-step), and per-run cost in
**[API_USAGE.md](API_USAGE.md)**.
