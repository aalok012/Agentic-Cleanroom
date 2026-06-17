# Agentic Cleanroom

A multi-agent pipeline that turns a **Software Requirements Specification (SRS)** into an
implementation plan — and ultimately **MVC source code** *and* **black-box tests** — where
the code generator and the test generator are **structurally forbidden from ever seeing
each other's work**, so the result can be **measured** as **pass@k** rather than tuned.

That isolation is the point of the project. In a normal "agentic coding" loop, tests are
run against the code and failures are fed back to fix the code, so the code slowly overfits
to the tests. Here there is **no feedback loop**: code is a pure function of the spec, tests
are a pure function of the spec, and the two are produced independently.

---

## The pipeline

Each agent is an `enrich(ir) -> ir` step that reads the shared **Intermediate
Representation (IR)** and folds in its own output — a clean, inspectable handoff. The
**front** of the pipeline (spec → dependency → planning) has been restructured to classify
requirements, build a *nested* dependency graph, and emit a **contract per requirement**:

```
  SRS.xml
    │
    ▼
  [1] Spec Agent ─────────► each feature's functional_requirements (FR) +
    │                       non_functional_requirements (NFR: category + rationale)
    │                       parse = deterministic · FR/NFR split = LLM (1 call / feature)
    ▼
  [2] Dependency Agent ───► ir["dependency_graph"] (OUTER, feature level) +
    │                       per-feature fr_order / fr_edges / fr_cycles (INNER, FR level)
    │                       cross-refs = deterministic · inner semantic edges = optional LLM
    ▼
  [3] Planning Agent ─────► ir["planning"].contracts — one CONTRACT per FR:
    │                       signature + docstring + mvc_layer + file_path + prerequisite_fr_ids
    │                       signature/docstring/layer = LLM · path & ordering = deterministic
    ▼
  [4] Code  [5] Test  [6] Certification   ← downstream; see note
```

| # | Agent | Folder | LLM? | Adds to IR | Responsibility |
|---|-------|--------|------|------------|----------------|
| 1 | **Spec** | `spec_agent/` | parse: No · classify: Yes | `features[].functional_requirements`, `features[].non_functional_requirements` | Parse the SRS XML deterministically (IDs/grouping never from the LLM), then one LLM call **per feature** labels each requirement **FR** or **NFR**; every NFR gets one of 8 categories + a rationale. Leaf sections (Security, Privacy…) are surfaced as one requirement so they're classifiable. |
| 2 | **Dependency** | `dependency/` | regex: No · inner semantic: optional | `dependency_graph` (outer) + `fr_order`/`fr_edges`/`fr_cycles` per feature (inner) | **Outer:** feature-level DAG + build order + cycles from explicit cross-references ("see section 2.5"); NFR-only features are never nodes. **Inner:** per-feature FR graph from the same regex; when an LLM is supplied it also infers semantic FR→FR prerequisites the prose implies. |
| 3 | **Planning** | `planning/` | Yes | `planning.contracts` | Walk the FRs in dependency order and emit a **contract per FR**: a concrete function **signature**, a **docstring** (behavior + the feature's NFR constraints), an **mvc_layer**, a deterministic **file_path**, and **prerequisite_fr_ids** from `fr_edges`. One LLM call per feature. |
| 4 | **Code** | `code/` | Yes | `generated_code` | One LLM call per increment, scoped to only that increment's requirements + prerequisite signatures. Writes MVC files. |
| 5 | **Test** | `test/` | Yes | `generated_tests` | One LLM call per feature, reading only `ir["features"]`. Derives black-box test cases from the spec. |
| 6 | **Certification** | `certification/` | Yes | `certification` | **pass@k.** Generates *n* code samples, judges each against the spec-derived tests, reports pass@k. Runs only after 4 & 5 are frozen. |

> **Note on stages 4–6.** The Code, Test and Certification agents still consume the legacy
> `increment_plan` and have **not yet been rewired** onto the new per-FR contracts, so
> `run_pipeline.py` currently **stops after Planning**. Their structural-isolation design and
> tests are intact (below); reconnecting them to `planning.contracts` is the next step.

### The isolation guarantee (enforced structurally, not by convention)

* The **Code Agent** has no public method parameter, import, or IR-key access that could
  carry test data. Its only input is the spec. There is no retry/debug loop.
* The **Test Agent** is the mirror image: it never imports the code agent and never reads
  `ir["generated_code"]` — all IR access goes through `spec_reader`, which touches only
  `ir["features"]`.
* **Certification** is the one place code and tests legitimately meet — and only **after
  both are frozen**. It feeds nothing back into generation.

Checked by `tests/test_code_agent.py` / `tests/test_test_agent.py`
(`TestStructuralIsolation` / `TestReadsOnlySpec`): a test injects poisoned `generated_code`
into the IR and asserts the generated tests come out **byte-identical**.

---

## Setup

**Prerequisites:** [uv](https://docs.astral.sh/uv/) and Python ≥ 3.11.

```bash
uv sync                                 # install deps into a local virtualenv
echo "OPENAI_API_KEY=sk-..." > .env     # only needed for real (non-stub) LLM runs
```

The XML parsing, cross-reference detection, build ordering, file-path mapping, and NFR
embedding are all deterministic. The **interpretive** steps — FR/NFR classification,
semantic inner edges, and signature/docstring/layer design — use `gpt-4o-mini`. You can run
the entire front pipeline **with zero tokens and no API key** using the stub LLMs (below).

---

## Quick start

### Run the front pipeline with the real model

```bash
uv run python run_pipeline.py "data/srs/2005 - phin.xml"
```

### Run it token-free (deterministic stubs — no key, no cost)

```bash
uv run python run_pipeline.py "data/srs/2005 - phin.xml" --stub-llm   # or: --no-llm
```

Either form writes:

* `outputs/2005 - phin_ir.json` — parsed features (base IR).
* `outputs/2005 - phin_fr_nfr.json` — the FR/NFR breakdown per feature.
* `outputs/2005 - phin_dependency.json` — outer graph + inner `fr_order`/`fr_edges`/`fr_cycles`.
* `outputs/2005 - phin_planning.json` — the per-FR contracts.
* `outputs/2005 - phin_full_ir.json` — the fully enriched IR + a `metrics` block.
* `outputs/2005 - phin_run_report.md` — per-stage timing, tokens, and cost.

If `OPENAI_API_KEY` is absent and no stub flag is given, the runner prints a warning and
falls back to the stubs so the front pipeline still completes.

### Verify the build

```bash
uv run pytest -q
```

---

## Running stages individually

```bash
# Stages 1 + 2 (no FR/NFR classification) → outputs/<name>_ir.json
uv run python main.py "data/srs/2005 - phin.xml"

# Dependency agent on a parsed IR (outer graph + inner regex edges; no LLM)
uv run python -m src.cleanroom.agents.dependency.agent "outputs/2005 - phin_ir.json"

# Planning agent on an enriched IR (prints the contracts)
uv run python -m src.cleanroom.agents.planning.agent "outputs/2005 - phin_dependency.json"
```

---

## Using your own SRS

The Spec Agent reads SRS documents in the **XML** format used by `data/srs/` (nested `<p>`
nodes with `<title>` and `<text_body>`, IDs like `2.2.6.6`). Drop your file in `data/srs/`
and point the pipeline at it; output filenames derive from the SRS filename stem.

```bash
uv run python run_pipeline.py "data/srs/your-spec.xml" --stub-llm
```

---

## Project layout

```
agentic-cleanroom/
├── run_pipeline.py            # front pipeline runner (+ --stub-llm) + run report; gates stages 4-6
├── main.py                    # stages 1–2 only (parse + dependency)
├── data/srs/                  # input SRS documents (XML)
├── outputs/                   # enriched IR JSON(s), run report, generated artifacts
├── tests/                     # pytest suite (incl. isolation invariants + pass@k math)
└── src/cleanroom/
    ├── agents/
    │   ├── spec_agent/         # [1] parse + FR/NFR classification  (prompts/classify_requirements.j2)
    │   ├── dependency/         # [2] nested graph                   (prompts/infer_fr_deps.j2)
    │   ├── planning/           # [3] per-FR contracts               (prompts/plan_feature.j2)
    │   ├── code/               # [4] spec → MVC code
    │   ├── test/               # [5] spec → black-box tests
    │   └── certification/      # [6] pass@k
    ├── llms/callbacks/         # metric.py — token/latency callback (auto-attached to every call)
    └── utils/                  # llm_client, prompt_renderer, logger, cost, code_stats
```

Each agent folder holds an `agent.py` and a `schema/` (Pydantic models); the LLM-assisted
agents also have `prompts/*.j2` and may have `tools/`.

---

## Design conventions

* **Deterministic-first.** The LLM is used only where genuine interpretation is needed
  (FR/NFR judgement, semantic prerequisites, signature/docstring/layer). Structure, IDs,
  grouping, cross-reference detection, file-path mapping, ordering, and NFR embedding are
  all plain code so they can never drift or hallucinate.
* **The LLM never owns IDs.** Requirement IDs always come from the parser; LLM output is
  matched back to known IDs and anything unrecognized is dropped.
* **Structured output, not prompt schemas.** LLM agents use
  `llm.with_structured_output(PydanticModel)` — the schema lives in code, not the prompt.
* **Token discipline.** One LLM call per unit of work (per feature). An agent is never
  handed the whole IR — only the scoped slice it needs.
* **The IR is the contract.** Every stage appends its keys and leaves prior keys untouched,
  so the full IR JSON is a complete, inspectable audit trail of the run.

---

## pass@k, briefly

pass@k is the HumanEval/Codex metric (Chen et al., 2021). For each feature we draw `n`
independent code samples; `c` of them pass **all** the feature's spec-derived test cases:

```
pass@k = mean_features( 1 - C(n - c, k) / C(n, k) )
```

Because the tests are natural-language designs, the pass/fail oracle is an LLM judge; any
sample the judge cannot confirm counts as a fail. (Applies to the downstream certification
stage once it is rewired onto the new contracts.)

---

## Status

The **front pipeline is restructured and tested**:

* **[1] Spec** — deterministic parse + per-feature **FR/NFR classification** with categories
  and rationale; leaf NFR sections (Security, Privacy, Vocabulary) are surfaced so they're
  classifiable.
* **[2] Dependency** — **nested** graph: deterministic outer (feature) DAG + inner
  (per-FR) graph, with an optional LLM pass that infers semantic FR→FR prerequisites; NFRs
  are constraints, never graph nodes.
* **[3] Planning** — a **contract per FR** (signature + docstring with embedded NFR
  constraints + MVC-aware file path + prerequisites), produced in dependency order.

The whole front runs **token-free** via `--stub-llm` (deterministic stubs) for inspection.

**Next step:** rewire the **Code / Test / Certification** stages to consume
`planning.contracts` instead of the legacy `increment_plan`, restoring the end-to-end
generate-and-measure (pass@k) flow on top of the new contract-based front.
```