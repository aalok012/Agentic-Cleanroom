# CLEANROOM-AGENT

**Generate an implementation from a Software Requirements Specification (SRS) and record, for each functional requirement, the evidence behind it: `PROVED`, `PROVED-WITH-AXIOMS`, `TESTED`, or `UNCERTIFIED`.**

CLEANROOM-AGENT is inspired by Cleanroom software engineering. It translates each functional requirement into a behavioral contract, generates code and tests without access to each other's output during initial generation, attempts to verify feature-level formal models with Dafny, and routes features to independent tests according to the verification outcome and target. A label records which evidence was obtained; it does not establish that the source requirement is fully satisfied.

---

## Contents

- [**How it works**](#how-it-works)
- [**Requirements**](#requirements) and [**Installation**](#installation)
- [**Quick start**](#quick-start)
- [**Reproducing the paper**](#reproducing-the-paper): RQ1–RQ4 and the human evaluation
- [**Results**](#results)
- [**Benchmark**](#benchmark)
- [**Repository layout**](#repository-layout)

---

## How it works

1. **Behavioral contracts.** A deterministic parser extracts requirements from structured XML; an LLM infers a contract (stimulus, precondition, response, postcondition) for each. Contracts are the pipeline's interpretation of the SRS, not guarantees.
2. **Independent derivation.** During initial generation, the Code Agent does not receive the generated tests, and the Test Agent does not receive the implementation. Both use the shared contracts and plan, so shared interpretation errors remain possible.
3. **Proof-first routing.** For each feature, the pipeline attempts to generate and verify a Dafny state model in a bounded generate–verify–revise loop. Test routing depends on the verification outcome and target (FastAPI/Express exclude verified features from testing; Spring excludes features that are verified and translated; plain Python/Java keep testing).
4. **Per-requirement labels.** `PROVED` means the generated feature model's stated proof obligations verified without explicit axioms; it is relative to the inferred contract and generated model, not the source SRS.

Stages: **Spec** → **Dependency analysis** → **Planning** (MVC placement) → **code / test / proof generation** → **certification** → optional **build repair and recovery** (recovery is Python-only and uses test feedback). Details: [`docs/methodology.md`](docs/methodology.md).

---

## Requirements

- **Python ≥ 3.11** and [**uv**](https://docs.astral.sh/uv/).
- An LLM API key: **OpenRouter** (used for all paper runs) or **OpenAI**.
- For the proof track: [**Dafny**](https://github.com/dafny-lang/dafny) on your `PATH`.
- For Java/Spring: a JDK and Maven. For JavaScript/Express: Node.js.

## Installation

```bash
uv sync
echo 'OPENROUTER_API_KEY=sk-or-...' > .env   # or OPENAI_API_KEY=sk-...
```

## Quick start

```bash
./run_example.sh
```

By default this runs the smallest subject (`Human.xml`, 2 FRs) with DeepSeek in Python. Override via environment variables:

```bash
MODEL=openai/gpt-5.1 LANG=java SRS="data/srs/dineout_srs.xml" ./run_example.sh
```

Or call the pipeline directly:

```bash
uv run python run_pipeline.py data/srs/Human.xml \
  --model deepseek/deepseek-v3.2 --language python \
  --prompt-strategy mot --prove --certify
```

Key flags: `--language {python,java,javascript}`, `--prompt-strategy {baseline,cot,mot}`, `--prove`, `--certify`, `--model`. Output goes to `--output-dir` (default `outputs/`).

---

## Reproducing the paper

All reported numbers are aggregated with [`scripts/collect_metrics.py`](scripts/collect_metrics.py) and archived under [`results/`](results/).

**RQ1: Effectiveness (pipeline vs. Baseline).**
```bash
uv run python run_pipeline.py <srs> --model <model> --language <lang> --prove --certify
uv run python run_baseline.py <srs> --model <model> --language <lang>
```

**RQ2: Prompting strategy (DeepSeek-V3.2).**
```bash
uv run python scripts/run_cot_experiment.py
uv run python scripts/run_mot_matrix_parallel.py
uv run python scripts/compare_three_way.py
```

**RQ3: Overhead.** Derived from `experiment_metrics.csv` (pipeline vs. Baseline rows).

**RQ4: Ablations (Qwen3-Coder-30B-A3B-Instruct-FP8, 4 subjects).** Results in `outputs/ablations/`.

**Human evaluation.** Ratings, adjudication, and agreement calculations for 50 sampled requirements are in `results/` (`Human_Evaluation_Cleanroom_agent.xlsx`).

---

## Results

Across 6 models, 3 languages, and 10 specifications (176 functional requirements):

- **RQ1:** average Verification Pass Ratio (VPR) rises from **38.8% to 67.5%**. Gains hold for every model family when averaged across languages, though not in every model–language combination. VPR measures model-level verification success, not correctness of the native implementation.
- **RQ2:** on DeepSeek-V3.2, Module-of-Thought prompting gives the highest PassVer@1 (69.5% to 78.0% vs. Zero-Shot), at about 20% more tokens and time.
- **RQ3:** the pipeline uses 5.47× tokens and 3.07× time per requirement; per-requirement cost generally decreases as specifications grow.
- **RQ4:** proof and verifier-guided repair account for most reported certification; in Java, test-based checks are compilation-based and produced no passing cases.
- **Human evaluation (50 random requirements, two authors):** 42/50 contracts correct and 40/50 complete, but only 16/50 generated models were faithful to the SRS, and 47/50 had unsupported assumptions.

Full tables and raw CSVs: [`results/`](results/) and [`docs/RUN_RESULTS.md`](docs/RUN_RESULTS.md).

---

## Benchmark

Ten SRS documents from the PURE corpus and other public sources, 2–54 functional requirements each (176 total), prepared as structured XML:

| Subject | Domain | Subject | Domain |
|---|---|---|---|
| `Human.xml` | student clubs event platform (2 FRs) | `Event Management.xml` | event management |
| `2009 - video search.xml` | video search | `TRADING SOFTWARE.xml` | stock trading |
| `0000 - gamma j.xml` | online shopping | `kinmail_srs.xml` | e-commerce marketplace |
| `0000 - cctns.xml` | crime and criminal tracking | `dineout_srs.xml` | restaurant ordering |
| `foodsaver.xml` | food-rescue platform | `Shoten_SRS.xml` | book sale and rental (54 FRs) |

Sources: [`data/srs/`](data/srs/).

---

## Repository layout
