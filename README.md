# Agentic Cleanroom

A multi-agent pipeline that turns a **Software Requirements Specification (SRS)** into **MVC source code** and **black-box tests**, with **structural isolation** between code generation and test generation so results can be measured with **pass@k** instead of tuned by a test-feedback loop.

In a typical agentic coding setup, failing tests are fed back into the code generator until tests pass — the code overfits to the tests. Here:

- **Code** is a pure function of the **specification** (plus optional **spec-level** contract violations from an independent reviewer).
- **Tests** are a pure function of the **specification** (requirements, behavioral contracts, planned interfaces).
- **Certification** is the only stage where code and tests meet — and only **after** both are frozen. It scores; it does not feed back into generation.

---

## Pipeline overview

The pipeline is **plain sequential Python** (`run_pipeline.py`). There is no graph framework. Each stage reads and extends a shared **Intermediate Representation (IR)** — a JSON document that accumulates artifacts as the run progresses.

```
  SRS.xml
    │
    ▼
  [1] Spec Agent          parse FRs (deterministic) + behavioral contracts (LLM)
    │
    ▼
  [2] Dependency Agent    nested dependency graph (regex + optional LLM)
    │
    ▼
  [3] Planning Agent      implementation contracts per FR (LLM + deterministic docstring)
    │
    ▼
  [4] Code Agent          one source file per FR (LLM)
    │
    ▼  (optional)
  [4b] Verification Agent reasoning-only contract review + bounded revise loop
    │
    ▼
  [5] Test Agent          black-box test cases from spec (LLM)
    │
    ▼  (optional)
  [6] Certification Agent pass@k scoring (executable oracle)
```

| Stage | Agent | LLM? | Adds to IR |
|-------|-------|------|------------|
| 1 | Spec | Parse: no · Contracts: yes (1 call/feature) | `features`, `contracts` |
| 2 | Dependency | Regex: no · Semantic FR edges: yes if LLM provided | `dependency_graph`, per-feature `fr_order` / `fr_edges` / `fr_cycles` |
| 3 | Planning | Yes (1 call/feature) | `planning.contracts` |
| 4 | Code | Yes (1 call/FR) | `generated_code` |
| 4b | Verification | Yes (1 call/FR; optional multi-pass) | `verification` |
| 5 | Test | Yes (1 call/feature) | `generated_tests` |
| 6 | Certification | Executable runner (optional extra code samples) | `certification` |

---

## The Intermediate Representation (IR)

Every stage appends keys to the same dict. The final artifact is `{project}_full_ir.json`.

| Key | Produced by | Contents |
|-----|-------------|----------|
| `project_name`, `source_file` | Spec (parse) | SRS stem and filename |
| `features[]` | Spec (parse) | Features with `functional_requirements[]` (`id`, `text`) |
| `contracts[]` | Spec (synthesize) | `BehavioralContract` per FR: stimulus, precondition, response, postcondition |
| `dependency_graph` | Dependency | Outer feature DAG: `nodes`, `edges`, `build_order`, `cycles` |
| `features[].fr_order` | Dependency | FR build order within a feature |
| `features[].fr_edges` | Dependency | Inner FR prerequisite edges |
| `features[].fr_cycles` | Dependency | FR-level cycles (if any) |
| `planning.contracts[]` | Planning | Per-FR `Contract`: signature, docstring, mvc_layer, file_path, prerequisites, embedded behavioral contract |
| `generated_code` | Code (+ optional verify/revise) | `files[]` with path, layer, content per FR |
| `verification` | Verification | Per-contract pass/fail, violations, rounds used |
| `generated_tests` | Test | Per-feature test cases + optional pytest source |
| `certification` | Certification | pass@k scores per feature and aggregate |
| `metrics` | Pipeline runner | Timing, tokens, cost per stage |

Intermediate snapshots are also written under `outputs/` (e.g. `{project}_ir.json`, `{project}_planning.json`, `{project}_contracts.json`).

---

## Agents (implementation detail)

### 1. Spec Agent — `src/cleanroom/agents/spec_agent/`

**Purpose:** Turn raw SRS XML into structured features and **behavioral contracts** (design-by-contract specs).

**Two phases:**

1. **`run()` — deterministic parse (no LLM)**  
   - Uses `SRSReader` (`tools/srs_reader.py`).  
   - Assigns stable IDs from the document structure.  
   - Groups functional requirements into features.  
   - **FR-only:** narrative sections (Introduction, Scope) and non-functional sections are ignored.  
   - Writes `outputs/{project}_ir.json`.

2. **`synthesize_contracts()` — LLM (one structured call per feature)**  
   - Prompt: `prompts/write_contract.j2`.  
   - For each FR, produces a `BehavioralContract`:
     - **stimulus** — what triggers the operation (input/event)
     - **precondition** — input constraints that must hold before execution
     - **response** — deterministic output
     - **postcondition** — guarantee after execution  
   - IDs are echoed verbatim from the parser; the LLM never invents them.  
   - Writes `outputs/{project}_contracts.json`.

**Supported SRS XML formats:**

| Format | Example | Extraction rule |
|--------|---------|-----------------|
| Legacy `req_document` | `data/srs/2009 - video search.xml` | Nested `<p>` nodes; requirements from sections titled **"Functional Requirements"** (`<itemize>` items → `REQ-N`) |
| `SystemRequirements` / `<Feature>` | `data/srs/dineout_srs.xml` | Each `<Feature id="..." name="...">` with a `<Description>` becomes one FR (`{id}.REQ-1`) |

**Schema:** `schema/ir.py` — `Feature`, `FunctionalRequirement`, `BehavioralContract`, `IntermediateRepresentation`.

---

### 2. Dependency Agent — `src/cleanroom/agents/dependency/`

**Purpose:** Build a **nested dependency graph** so downstream agents process requirements in a safe build order.

**Outer graph (feature level):**

- Nodes = features that have functional requirements.
- Edges = explicit cross-references in requirement text (e.g. `"see section 2.2"`).
- Informational pointers (`"more information found in section X"`) are **filtered out** — they are not build prerequisites.
- Produces `build_order` and detects `cycles`.

**Inner graph (FR level, per feature):**

- Same cross-reference detection within a feature.
- Optional LLM pass (`prompts/infer_fr_deps.j2`) infers semantic FR→FR prerequisites the prose implies.
- Each feature gets `fr_order`, `fr_edges`, `fr_cycles`.

**Edge convention:** `source` depends on `target` → `target` must be built **before** `source`.

**Entry point:** `DependencyAnalyzer.enrich(ir)` → adds `dependency_graph` and inner fields on `features[]`.

---

### 3. Planning Agent — `src/cleanroom/agents/planning/`

**Purpose:** Attach **implementation metadata** to each behavioral contract — the interface the Code Agent will implement.

**Input:** `ir['features']`, `ir['contracts']`, `ir['dependency_graph']` (for ordering and prerequisites).

**Output:** One `Contract` per FR in `planning.contracts[]`:

| Field | Source |
|-------|--------|
| `signature` | LLM (concrete Python function signature) |
| `args`, `returns` | LLM (for Google-style docstring) |
| `mvc_layer` | LLM (`model` \| `view` \| `controller`; keyword fallback if invalid) |
| `docstring` | **Deterministic** — Google/Napoleon style assembled from behavioral contract + prerequisites |
| `file_path` | **Deterministic** — `{models\|views\|controllers}/{func_name}.py` |
| `prerequisite_fr_ids` | **Deterministic** — from `fr_edges` |
| `contract` | Embedded copy of the `BehavioralContract` |

**LLM:** One call per feature via `prompts/plan_feature.j2` + `with_structured_output(FeaturePlan)`.

**Stack awareness:** For `--stack fastapi`, signatures are shaped as FastAPI route handlers with typed parameters, SQLAlchemy model functions, or view payloads.

**Deterministic-first:** Ordering, IDs, paths, docstring structure, and prerequisite notes are plain code.

---

### 4. Code Agent — `src/cleanroom/agents/code/`

**Purpose:** Generate one **source file body** per planning contract.

**Input (spec-derived only):**

- This FR's contract: signature, docstring, requirement text.
- **Prerequisite signatures only** — never prerequisite file bodies, never tests.

**Methods:**

- **`generate(ir)`** — one LLM call per contract (`prompts/generate_code.j2`); returns `GeneratedCode`.
- **`revise(ir, contract, prior_content, violations)`** — revision from **spec-level contract violations** only (`prompts/generate_code_revision.j2`). Used by the Verification loop. Never accepts test cases or expected outputs.

**Output:** `generated_code.files[]` — each entry has `fr_id`, `path`, `mvc_layer`, `content`.

**Isolation (structural):**

- No parameter or IR access path for test data.
- Does not import or read `generated_tests`.
- `revise()` is the only feedback channel — and only from the Verification Agent's contract-clause violations.

**Packaging (`--stack fastapi`):** `utils/packager.py` assembles files into a runnable FastAPI app (`app/`, router registration, model de-duplication, `requirements.txt`).

---

### 5. Verification Agent — `src/cleanroom/agents/verification/`

**Purpose:** Independent, **reasoning-only** reviewer that checks whether generated code satisfies its spec-derived contract. Does **not** execute code.

**Input:**

- `ir['features']`, `ir['contracts']`, `ir['planning']['contracts']`
- Generated file content under review

**Never reads:** `generated_tests`, Test Agent imports, or any runtime execution.

**Method:** `verify_code(ir, code, only_fr_ids=None)` → list of `ContractVerdict` per FR.

**Prompt:** `prompts/verify_contract.j2` — adversarial cold read; checks signature, stimulus, precondition, response, postcondition, prerequisite calls, coverage.

**Violations** use a fixed clause taxonomy (`precondition`, `stimulus`, `response`, `postcondition`, `signature`, `prerequisite_call`, `coverage`) — no fields for test inputs or expected outputs.

**Bounded loop** (`verification/loop.py` — `generate_and_verify()`):

```
generate all files
  → verify all contracts
  → for up to max_rounds:
       revise each failing file (CodeAgent.revise)
       re-verify only changed files
  → return (GeneratedCode, VerificationResult)
```

Used by **both** `run_pipeline.py` stage 4 (when `--verify`) and `CertificationAgent` (when certifying with `--verify`).

**Flags:** `--verify`, `--verify-rounds`, `--verify-model`, `--verify-passes` (>1 requires unanimous fail before revising).

---

### 6. Test Agent — `src/cleanroom/agents/test/`

**Purpose:** Derive **black-box test cases** from the specification — one LLM call per feature.

**Input (via `test/tools/spec_reader.py` — spec-stage only):**

- `ir['features']` — requirement text
- `ir['contracts']` — behavioral contracts (stimulus, response, postcondition, …)
- `ir['planning']` — planned signatures and layers (same interface the Code Agent targets)

**Never reads:** `generated_code`, `generated_tests`.

**Output:** `generated_tests.features[]` — structured `cases` (certification oracle) plus optional `pytest_source` modules written to `outputs/generated/{project}/tests/test_feature_*.py`.

**Isolation:** Tests and code agree by anchoring to the **same contracts**, not by the Test Agent seeing implementation.

---

### 7. Certification Agent — `src/cleanroom/agents/evaluation/`

**Purpose:** **pass@k** (default **pass@1**) — the only stage where code and tests meet.

**Process:**

1. Load spec-derived test cases (`generated_tests`).
2. Use stage-4 code as sample 0; generate `samples - 1` extra only when `samples > 1`.
3. **Executable oracle:** subprocess runs each case (`inputs_json` / `expected_json`) per FR.
4. A sample **passes** an FR only if **all** its cases pass.
5. Macro-average pass@k over FRs (HumanEval-style task units).

**Metric:** `pass@k = mean_FR( c/n )` when k=1; unbiased estimator for k>1.

**Output:** `certification` in IR + `certification_report.md`.

**Isolation:** Scores frozen artifacts only; no feedback to Code or Test agents.

---

## Clean-room isolation (summary)

```
                    ┌─────────────┐
                    │     SPEC    │
                    │ (SRS + IR)  │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
      Code Agent      Test Agent     Verification
      (spec only)     (spec only)    (spec + code under review;
           │               │          spec-level feedback only)
           │               │
           └───────┬───────┘
                   ▼
            Certification
         (executable oracle — no feedback)
```

| Agent | May read | Must never read |
|-------|----------|-----------------|
| Code | spec, planning contracts, contract violations | `generated_tests`, test failures |
| Test | features, contracts, planning | `generated_code` |
| Verification | spec, planning, code under review | `generated_tests`; no execution |
| Certification | spec tests + code samples | (scores only; no write-back) |

---

## Changelog

Recent pipeline changes (executable certification, python stack defaults, DineOut results) are documented in **[CHANGES.md](CHANGES.md)**.

**Quick reference — certification:**

```bash
# pass@1
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --stack python --certify --samples 1

# pass@1 + pass@3
uv run python run_pipeline.py "data/srs/dineout_srs.xml" --stack python --certify --samples 3
```

---

## Setup

**Prerequisites:** [uv](https://docs.astral.sh/uv/), Python ≥ 3.11, OpenAI API key.

```bash
uv sync
echo "OPENAI_API_KEY=sk-..." > .env
```

Default model: **gpt-4o-mini** (`src/cleanroom/utils/llm_client.py`).

---

## Running the pipeline

### Basic (spec → code → tests)

```bash
uv run python run_pipeline.py "data/srs/dineout_srs.xml"
```

### With verification (review + revise loop)

```bash
uv run python run_pipeline.py "data/srs/dineout_srs.xml" \
  --verify --verify-rounds 2
```

| Flag | Default | Meaning |
|------|---------|---------|
| `--verify` | off | Enable Verification Agent + revise loop after code generation |
| `--verify-rounds` | 2 | Max revise rounds (`0` = verify only, no revise) |
| `--verify-model` | gpt-4o-mini | Model for the reviewer |
| `--verify-passes` | 1 | Reviewer passes per contract; >1 requires unanimous fail |
| `--certify` | off | Run pass@k certification (executable oracle) |
| `--samples` | 3 | Code samples per FR for pass@k |
| `--stack` | python | Target stack (`python` or `fastapi`) |
| `--output-dir` | outputs | Artifact directory |

### Run individual agents

```bash
# Spec only
uv run python -m src.cleanroom.agents.spec_agent.agent data/srs/dineout_srs.xml

# Planning on enriched IR
uv run python -m src.cleanroom.agents.planning.agent outputs/dineout_srs_planning.json

# Certification on full IR
uv run python -m src.cleanroom.agents.evaluation.agent outputs/dineout_srs_full_ir.json
```

---

## Outputs

After `run_pipeline.py`:

| Path | Description |
|------|-------------|
| `outputs/{project}_ir.json` | Parsed features (after stage 1 parse) |
| `outputs/{project}_contracts.json` | Features + behavioral contracts |
| `outputs/{project}_dependency.json` | IR + dependency graph |
| `outputs/{project}_planning.json` | IR + planning contracts |
| `outputs/{project}_full_ir.json` | Complete enriched IR + metrics |
| `outputs/{project}_run_report.md` | Timing, tokens, cost, verification/cert summary |
| `outputs/generated/{project}/app/` | Runnable FastAPI package (`--stack fastapi`) |
| `outputs/generated/{project}/tests/` | Pytest modules (`test_feature_*.py`) |
| `outputs/generated/{project}/verification_report.md` | Per-contract verify results (if `--verify`) |
| `outputs/generated/{project}/certification_report.md` | pass@k report (if `--certify`) |

---

## Project layout

```
agentic-cleanroom/
├── run_pipeline.py                 # End-to-end pipeline runner
├── data/srs/                       # Input SRS documents (XML)
├── outputs/                        # IR JSON, reports, generated artifacts
└── src/cleanroom/
    ├── agents/
    │   ├── spec_agent/             # [1] Parse + behavioral contracts
    │   │   ├── agent.py
    │   │   ├── schema/ir.py
    │   │   ├── tools/srs_reader.py
    │   │   └── prompts/write_contract.j2
    │   ├── dependency/             # [2] Nested dependency graph
    │   ├── planning/               # [3] Implementation contracts
    │   ├── code/                   # [4] Source generation + revise
    │   ├── verification/           # [4b] Contract reviewer + loop
    │   ├── test/                   # [5] Black-box tests
    │   └── evaluation/             # [6] pass@k certification
    ├── llms/callbacks/metric.py    # Token/latency tracking (all LLM calls)
    └── utils/
        ├── llm_client.py           # OpenAI / LangChain client
        ├── prompt_renderer.py      # Jinja2 prompt loading
        ├── packager.py             # FastAPI app assembly
        ├── code_stats.py           # LOC / layer stats
        └── cost.py                 # Token cost estimation
```

Each agent folder contains:

- `agent.py` — main logic
- `schema/` — Pydantic models for structured LLM output and IR slices
- `prompts/*.j2` — Jinja2 templates (where LLM is used)
- `tools/` — deterministic helpers (where applicable)

---

## Design principles

1. **Deterministic-first** — IDs, parsing, grouping, ordering, file paths, and docstring assembly are plain code. The LLM is used only for interpretation (contracts, signatures, code bodies, tests, review).

2. **The LLM never owns IDs** — Requirement IDs always come from the parser. LLM output is matched by echoed id; unrecognized ids are dropped.

3. **Structured output** — `llm.with_structured_output(PydanticModel)`; schemas live in Python, not in prompts.

4. **Token discipline** — One LLM call per unit of work (per feature or per FR). Agents are never handed the whole IR — only the scoped slice they need.

5. **The IR is the audit trail** — Every stage appends keys; `{project}_full_ir.json` is a complete record of the run.

6. **Structural isolation** — Code and tests cannot see each other's artifacts by construction. Verification feedback is spec-level only. Certification scores without feeding back.

---

## Rough timing (gpt-4o-mini, sequential)

Times scale with **number of FRs** and **LLM calls** (~4–5 s per call).

| Configuration | ~10 FRs | ~16 FRs |
|---------------|---------|---------|
| Default (no verify, no certify) | 1–2 min | 2–3 min |
| `--verify --verify-rounds 1` | 3–4 min | 5–6 min |
| `--verify --verify-rounds 2` | 4–5 min | 7–8 min |
| `--verify --verify-rounds 1 --certify --samples 1` | 8–12 min | 10–15 min |
| `--verify --verify-rounds 2 --certify --samples 3` | 15–20 min | 25–35 min |

Certification with `--verify` regenerates code samples when `--samples > 1`, which dominates cost.

---

## Reading results in Python

```python
import json
from src.cleanroom.agents.evaluation.schema.certification import CertificationResult
from src.cleanroom.agents.verification.schema.verification import VerificationResult

ir = json.load(open("outputs/dineout_srs_full_ir.json"))

if "verification" in ir:
    v = VerificationResult(**ir["verification"])
    print(v.n_passing, "/", v.n_contracts, "contracts pass")

if "certification" in ir:
    c = CertificationResult(**ir["certification"])
    print(c.aggregate_pass_at)
    print(c.aggregate_case_pass_rate)
```

---

## License / status

This is a research/engineering pipeline for **clean-room code generation measurement**. The front pipeline (spec → dependency → planning) and downstream stages (code, verification, test, certification) are wired end-to-end via `run_pipeline.py` and the shared IR.
