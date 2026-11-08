# CLEANROOM-AGENT

**Generate application code from a Software Requirements Specification (SRS) and record per-requirement evidence from generated feature models and tests.**

This README documents the implementation and available materials for **CLEANROOM-AGENT: Per-Requirement Evidence for LLM-Generated Applications**, submitted to **ICSE 2027 SEIP**. The system attempts verification and testing; it does not promise a fully working application. Evidence labels describe the checks obtained, subject to the proof and reporting limits below.

## Contents

- [How it works](#how-it-works)
- [Proof boundary and evidence labels](#proof-boundary-and-evidence-labels)
- [Installation](#installation)
- [Usage](#usage)
- [Metrics](#metrics)
- [Submitted results](#submitted-results)
- [Benchmark](#benchmark)
- [Available materials and remaining gaps](#available-materials-and-remaining-gaps)

## How it works

1. **Extract requirement records.** The authors prepared the benchmark documents as structured XML. The [deterministic XML reader](src/cleanroom/agents/spec_agent/tools/srs_reader.py) extracts functional requirement text, identifiers, and grouping from that structure. This is not automatic semantic interpretation of arbitrary SRS PDFs.
2. **Infer behavior and plan.** An LLM interprets each extracted requirement as a behavioral contract (stimulus, precondition, response, postcondition). Dependency analysis and MVC-oriented planning guide artifact generation. These inferred contracts and plans can omit behavior or introduce unsupported assumptions; extraction fidelity does not establish their adequacy.
3. **Generate artifacts independently at first.** During initial generation, code generation cannot access generated tests, and test generation cannot access the generated implementation. Both share behavioral specifications and plans. This separation prevents direct cross-artifact access during that phase, but shared specifications can introduce correlated errors.
4. **Attempt proof, then route tests.** A bounded Dafny generate–verify–revise loop checks feature models before code generation. FastAPI uses adapters over compiled Dafny cores for proved features; Spring adapts features only when proof and Java translation succeed. Express generates native code and excludes proved features from certification even though it ships no Dafny-core adapter. Plain Python/Java stacks retain testing of proved features. These routing choices can leave integration behavior untested.
5. **Certify and optionally recover.** Certification combines generated code and tests. Controlled recovery can use failing-test feedback to regenerate implementation and retry proof/testing; this relaxes initial generation isolation. Recovery is implemented for Python and recorded separately in recovery fields and loop records, with reporting caveats below.

See [methodology](docs/methodology.md) and the [pipeline implementation](run_pipeline.py) for further detail. Some implementation comments and older documentation make stronger correctness claims than the proof boundary supports.

## Proof boundary and evidence labels

**Dafny verifies stated obligations of generated feature models relative to their inferred formalization.** Feature-level proof credit is attributed to the requirements associated with that feature; it does not demonstrate that every associated requirement is fully represented in the obligations. Coverage can be partial or vacuous and is not quantified.

A `PROVED` result does **not** establish full inferred-contract coverage, source-SRS satisfaction, or end-to-end application correctness. Adapters, databases, interfaces, and external behavior remain outside the proof boundary, including when generated application code invokes a compiled model core. A verified model unrelated to native code provides no correctness guarantee for that code.

The submission uses these evidence categories:

| Label | Meaning |
|---|---|
| `PROVED` | The associated feature model's stated obligations verified without explicit admitted axioms. This does not mean that the model contains no unsupported semantic assumptions. |
| `PROVED-WITH-AXIOMS` | Verification succeeded while relying on explicitly admitted axioms; those assumptions were not discharged by the proof. |
| `TESTED` | In the absence of proof credit, all associated generated test cases passed for the assessed sample. The strength of this evidence depends on the oracle and target; Java checks here are compilation-based. |
| `UNCERTIFIED` | Neither proof credit nor a complete passing-test result was obtained. Missing or failed checks do not establish correctness. |

Recovery is provenance, not a fifth evidence category. Initial and post-recovery outcomes should be reported separately.

**Implementation/reporting discrepancy.** The checkout retains per-feature `verified` and `axioms` data and an aggregate `n_proved_with_axioms`, but its report and recovery label paths commonly emit `PROVED` for both proof categories. Without recovery, the final label table may list only proved features rather than all four outcomes. The [ablation summarizer](scripts/summarize_reviewer_ablations.py) reconstructs requirement labels from saved proof/test fields, using spellings `PROVED_WITH_AXIOMS` and `TESTED_PASS`. Thus the four distinctions described in the paper are not consistently preserved as explicit labels in every pipeline report. Inspect axiom counts, test outcomes, and requirement-to-feature mappings rather than relying on the displayed label alone.

Recovery records are separate, but recovery updates the proof set and certification results used to compute the final summary. Consequently, a saved `metrics.summary["PassVer@1"]` can include recovery outcomes rather than initial certification alone. Initial values require a preserved pre-recovery snapshot or an explicit reconstruction with sufficient saved evidence; the final field name alone is insufficient.

## Installation

Requirements: Python **3.11 or later**, [uv](https://docs.astral.sh/uv/), and an LLM API key. Install [Dafny](https://github.com/dafny-lang/dafny) on `PATH` for proof generation/verification and the appropriate target toolchain: JDK/Maven for Java/Spring, Node.js for JavaScript/Express. Plain Java test-source compilation may also require `JUNIT_JAR`.

From the repository root:

```bash
uv sync
```

Add the appropriate key to `.env` or export it in your shell:

```dotenv
OPENROUTER_API_KEY=your-key
```

The client automatically uses OpenRouter when only `OPENROUTER_API_KEY` is set. Direct OpenAI use instead requires `OPENAI_API_KEY` and an appropriate OpenAI model name. If both keys are set, OpenAI configuration takes precedence. See the [client implementation](src/cleanroom/utils/llm_client.py) for `OPENAI_BASE_URL` and request timeout/retry configuration. The paper's six-model study used OpenRouter; the ablation manifest records a separate Qwen setup.

## Usage

The [example wrapper](run_example.sh) defaults to `Human.xml`, DeepSeek-V3.2, and MoT prompting. Set `LANG` explicitly because shells commonly already define it as a locale:

```bash
LANG=python ./run_example.sh
MODEL=openai/gpt-5.1 LANG=java SRS=data/srs/dineout_srs.xml ./run_example.sh
```

Direct invocation makes the target stack and recovery policy explicit:

```bash
uv run python run_pipeline.py data/srs/Human.xml \
  --model deepseek/deepseek-v3.2 --language python --stack fastapi \
  --prompt-strategy mot --prove --certify --samples 1 --k 1 \
  --no-recovery --output-dir outputs/example
```

Supported options include `--language {python,java,javascript}`, `--stack {auto,python,fastapi,java,spring,express}`, `--prompt-strategy {baseline,cot,mot}`, `--prove`, `--prove-rounds`, `--certify`, `--samples`, `--k`, `--recovery`/`--no-recovery`, `--max-cert-loops`, `--max-compile-repair-loops`, per-stage model overrides, and `--resume`. Proof and certification default off; recovery defaults on when applicable, with at most two certification recovery loops. Use `--no-recovery` to preserve an initial-only assessment.

```bash
uv run python run_pipeline.py --help
uv run python run_baseline.py --help
```

Outputs include generated artifacts, `*_full_ir.json`, `*_run_report.md`, and `runs/*.json` under the selected output directory (default `outputs/`). Pipeline runs also update documentation ledgers; choose destinations carefully when conducting new experiments. No experiments were rerun to prepare this README.

## Metrics

| Metric | Unit and interpretation |
|---|---|
| **VPR** (Verification Pass Ratio) | Requirements credited through verified feature models / all requirements. Each associated requirement inherits the feature's proof outcome, including axiom-dependent credit where counted. It measures model-level verification evidence, not native-code correctness. |
| **TPR** (Test Pass Ratio) | Individual passing test-case executions / test-case executions on the target's test track. Partial case credit differs from a requirement passing all its cases. |
| **PASSVER@1** (`PassVer@1` in saved fields) | Requirements credited by proof **or** by passing all associated tests for the initial sample / all requirements, deduplicating overlap. This is initial certification in the paper; saved post-recovery summaries need the qualification above. |
| **Input/output tokens per call** | Total input/output tokens divided by LLM calls. These two means do not sum to total tokens per run. |
| **Total tokens per run; overhead per requirement** | Sum of input and output tokens across calls in a run; divide run tokens and wall-clock time by requirement count for per-requirement overhead. Table II reports total run tokens in thousands. |

Baseline and pipeline TPR use different evidence and populations and are **not directly comparable**. The baseline generates runnable test files for unproved features; the pipeline uses structured test cases under target-specific routing. Java/Spring certification uses `javac`/Maven test compilation rather than execution of behavioral assertions. Test oracles have not been independently validated. VPR should also be distinguished from feature-count `dafny_verification_rate`; the collector can fall back to the latter for older baseline records lacking requirement-level data.

The direct-generation [baseline](run_baseline.py) uses LLM feature extraction from raw SRS text, generates native code directly, and also generates a Dafny model in one pass by default (`--prove-rounds 1`). It has no contract-inference, dependency/planning, or recovery stages. Its model is generated separately from the native implementation: verification measures **model-level proof success**, not native-code correctness. The pipeline's `--baseline` preset is a different control (proof/recovery off and simplified dependencies), not this direct-generation baseline.

## Submitted results

These are the submitted paper's reported aggregates, not newly recomputed experimental results. The benchmark has ten specifications and 176 functional requirements, with six models and three target languages. The six models are Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.1, Gemini 3.1 Pro, Gemini 3 Flash, and DeepSeek-V3.2.

- **RQ1, effectiveness:** Table I reports average VPR **38.82% → 67.48%**, a gain of **28.66 percentage points**. Gains hold across model families averaged over languages, but not every model–language combination. Of 180 planned pipeline configurations, **125 completed**; 55 did not finish because of provider timeouts/rate limits. Table I averages completed runs. Across 2,341 requirement instances, pooled initial counts are **1,274 PROVED, 41 PROVED-WITH-AXIOMS, 247 TESTED, 779 UNCERTIFIED**; post-recovery counts are **1,385, 56, 247, 653**, respectively. These pooled counts are not the same aggregation as Table I's per-setting averages.
- **RQ2, prompting:** On DeepSeek-V3.2, Zero-Shot/CoT/MoT PASSVER@1 is **69.50% / 75.58% / 78.03%**. MoT VPR is **64.65%** and TPR **41.97%**. Relative to Zero-Shot, MoT consumes **19.8%** more tokens and **18.1%** more time.
- **RQ3, overhead:** Table III reports **25.5K vs. 4.7K tokens per requirement (5.47×)** and **88.7 vs. 28.9 seconds per requirement (3.07×)**. Per-requirement costs generally decrease with specification size; this is an observed trend, not a guarantee.
- **RQ4, ablations:** Table IV's repeat-1 full-pipeline PASSVER@1 is **50.4% / 47.2% / 63.8%** for Python/Java/JavaScript. Removing proof reduces it to **5.7% / 0.0% / 38.6%**. In JavaScript, removing independent tests reduces it to **49.2%**, while exposing code to test generation raises it to **84.3%**, consistent with possible validation leakage rather than established correctness. No Java compilation-based cases passed (**0/905**). Single-run ablation differences must be interpreted alongside full-pipeline variation.
- **RQ5, human evaluation:** Two authors independently assessed 50 sampled requirements and adjudicated disagreements. **42 contracts were judged correct, 40 complete, 16 formal models faithful, and 47 models contained unsupported assumptions.** The random sample spans verified and unverified models across the ten subjects, six models, and three languages. These are **not rates specifically for PROVED models** and do not measure the predictive accuracy of proof labels.



## Benchmark

The authors prepared ten public SRS documents, from PURE and other sources, into [structured XML](data/srs/): 2–54 functional requirements each, 176 total.

| Subject | Domain |
|---|---|
| `Human.xml` | Student clubs event platform (2 FRs) |
| `2009 - video search.xml` | Video search |
| `Event Management.xml` | Event management |
| `TRADING SOFTWARE.xml` | Stock trading |
| `0000 - gamma j.xml` | Online shopping |
| `kinmail_srs.xml` | E-commerce marketplace |
| `0000 - cctns.xml` | Crime and criminal tracking |
| `dineout_srs.xml` | Restaurant reservation service |
| `foodsaver.xml` | Food-rescue platform |
| `Shoten_SRS.xml` | Book sale and rental (54 FRs) |


The available materials support inspection and partial reconstruction, **not complete reproduction of the submission**.
