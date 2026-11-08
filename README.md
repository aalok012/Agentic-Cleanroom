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
- [Reproduction guidance: RQ1–RQ5](#reproduction-guidance-rq1rq5)
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

## Reproduction guidance: RQ1–RQ5

The commands below describe available entry points; they do not imply that all submitted tables can be regenerated from this checkout. Use fresh output locations for any new runs and preserve archived results. Missing materials and implementation discrepancies are listed explicitly.

### RQ1: Effectiveness

Run the pipeline and direct-generation baseline on the same SRS, model, and language, selecting the matching pipeline stack. For example:

```bash
uv run python run_pipeline.py data/srs/Human.xml \
  --model deepseek/deepseek-v3.2 --language python --stack fastapi \
  --prompt-strategy baseline --prove --certify --samples 1 --k 1 \
  --no-recovery --output-dir outputs/reproduction/rq1/pipeline/python/Human/deepseek
uv run python run_baseline.py data/srs/Human.xml \
  --model deepseek/deepseek-v3.2 --language python --prove-rounds 1 \
  --output-dir outputs/reproduction/rq1/baseline/python/Human/deepseek
uv run python scripts/collect_metrics.py \
  --root outputs/reproduction/rq1/pipeline --out /tmp/cleanroom-pipeline-metrics.csv
uv run python scripts/collect_metrics.py \
  --root outputs/reproduction/rq1/baseline --out /tmp/cleanroom-baseline-metrics.csv
```

These are initial-only example runs, not an exact reconstruction of every submitted configuration. Preserve initial snapshots before evaluating recovery separately. The collector supports `--root`, `--out`, and `--append`; it aggregates saved records rather than generating the paper's tables. Available aggregate inputs include [experiment metrics](results/raw_results/experiment_metrics.csv), [baseline metrics](results/raw_results/baseline_metrics.csv), [additional baseline metrics](results/raw_results/baseline_runpy_newmodels_metrics.csv), [additional model metrics](results/raw_results/newmodels_metrics_current.csv), and [passk matrix metrics](results/raw_results/passk_matrix_metrics.csv). These CSVs contain different run populations; do not concatenate them without identifying configurations, duplicates, completion status, and recovery stage. A complete submitted-run selection manifest and the complete RQ1 raw run artifacts are absent.

Additional local audit helpers exist: [Table I reconciliation](scripts/check_rq1_table.py), [label reconstruction](scripts/audit_label_distributions.py), [archive PASSVER reconstruction](scripts/report_archived_passver.py), and [Table I PASSVER report](scripts/report_table1_passver.py). These are currently untracked analysis scripts, not a complete submitted-table reproduction workflow. The label auditor points to external Desktop archives, and the PASSVER reporters require files under `results/reviewer_audit/` that are absent here. The Table I PASSVER reporter expects 107 selected pipeline runs, whereas the submission describes 125 completed runs; that population discrepancy requires reconciliation before claiming exact reproduction.

### RQ2: Prompting

The available drivers launch new experiments:

```bash
uv run python scripts/run_cot_experiment.py
uv run python scripts/run_mot_matrix_parallel.py
```

Both use DeepSeek-V3.2 across XML subjects and Python/FastAPI, Java/Spring, JavaScript/Express, with `--prove --certify --max-cert-loops 4 --prove-rounds 4`. CoT settings include `COT_CELL_TIMEOUT` (3900 seconds) and `COT_MAX_ROUNDS` (4). MoT settings include `MOT_CONCURRENCY` (2), `MOT_TIMEOUT_MIN` (**180 in code**, despite an older docstring saying 120), and `MOT_MAX_ATTEMPTS` (3). Initial-only comparisons can instead use the direct pipeline command with `--prompt-strategy baseline`, `cot`, or `mot` and `--no-recovery`; the archived drivers' recovery policy must be accounted for when interpreting their summaries.

Archived inputs/results: [CoT](results/raw_results/cot_deepseek_results.csv), [MoT](results/raw_results/mot_deepseek_results.csv), [three-way comparison](results/raw_results/three_way_deepseek.csv), and [summary](results/raw_results/three_way_summary_deepseek.csv). The [comparison script](scripts/compare_three_way.py) has no CLI path options and expects `experiment_metrics.csv`, `cot_deepseek_results.csv`, and `mot_deepseek_results.csv` at the repository root, whereas the archives are under `results/raw_results/`. It writes root-level comparison CSVs and can fall back to `outputs/mot/` for MoT data. It is not a drop-in command for the archived layout; stage copies of its inputs in a separate checkout before running `uv run python scripts/compare_three_way.py`. Complete original prompting-run artifacts and a selection manifest are missing.

### RQ3: Overhead

Use the RQ1 collector on saved run records, then normalize `tokens_total` and `total_seconds` by `n_frs`. Keep per-call averages separate from run totals and reproduce the paper's subject/model/language averaging rather than treating pooled tokens as an average. The archived metric CSVs supply aggregate cost fields, but a complete Table III/Figure 2 selection manifest and dedicated table/figure-generation script are not present. The collector alone does not regenerate those displays.

### RQ4: Ablations and Table IV

The submitted design uses **Human (2 FRs), Video Search (7), Event Management (12), and Shoten (54)**: 75 requirements per language, 225 across **Python, Java, and JavaScript**, with **Qwen3-Coder-30B-A3B-Instruct-FP8**. The full pipeline runs **three repeats**; each ablation runs once per subject/language. Compare ablations against **full-pipeline repeat 1**. Table IV macro-averages over subjects and reports the full-pipeline mean and **sample** standard deviation across three repeats.

The five submitted ablations are: tests see code; no independent tests; no proof; raw specification only (contracts and planning removed together); and no verifier-guided repair (proof revision and Java compile repair disabled). The two test-related ablations reuse repeat-1 proof artifacts, so their unchanged VPR does not represent a new independent proof trial.

The local archive is [outputs/ablation/minsky_qwen3coder_fp8/](outputs/ablation/minsky_qwen3coder_fp8/), with a [manifest](outputs/ablation/minsky_qwen3coder_fp8/manifest.json) and [summary CSV](outputs/ablation/minsky_qwen3coder_fp8/ablation_results.csv). This is **singular `ablation`**, unlike the original machine's `outputs/ablations/` paths embedded in the manifest. It contains Python runs only: 36 manifest entries (12 reference repeats and four runs for each of six arms, including an extra `with_recovery` arm outside Table IV's five ablations). There are 35 local full-IR files; Shoten's `with_recovery` full IR is missing although the saved summary marks 36 runs complete. Java and JavaScript ablation raw results/manifests are absent here. These local, ignored output artifacts are not tracked in Git and may be absent from a fresh clone.

The added script is **[scripts/summarize_reviewer_ablations.py](scripts/summarize_reviewer_ablations.py)**. It **summarizes saved runs; it does not launch ablations**. Its only argument is a positional JSON `manifest` (plus standard `-h`/`--help`); it has no `--root`, `--out`, or experiment-selection flags:

```bash
python3 scripts/summarize_reviewer_ablations.py --help
# After relocating a COPY of the manifest's output_dir paths to existing local runs:
python3 scripts/summarize_reviewer_ablations.py /tmp/cleanroom-ablation-review/manifest.json
```

The manifest must contain `runs`, each with `subject`, `language`, `arm`, `stem`, and `output_dir`, plus optional model/repeat/reuse/exit-status fields. Each run is read from `<output_dir>/<stem>_full_ir.json`. The supplied manifest's `/home/cfw36/...` paths do not exist locally and must be remapped in a scratch copy before summarization. For this archive, map the final subject/language/arm directories beneath the actual local archive root; put the copied manifest in a scratch directory so archived CSVs are preserved.

The script writes `ablation_results.csv`, `ablation_fr_labels.csv`, `ablation_stages.csv`, and `ablation_recovery.csv` beside its input manifest. It reconstructs evidence counts and denominators, emits saved cost/stage/recovery fields, and marks missing/invalid runs; oracle-based fields remain blank without saved oracle data. It raises an error if reconstructed VPR or PASSVER@1 disagrees with the saved summary. Its reference noise band is grouped by subject/language and uses **population** SD (`statistics.pstdev`), not Table IV's sample SD after subject aggregation. It therefore does not generate Table IV directly.

**Runner gap:** no ablation execution driver is present. The archived commands use `--test-sees-code`, `--raw-spec-only`, `--reuse-from`, and `--reuse-stages`, which the current pipeline CLI does not support. The archived `no_verifier_repair` command sets `--prove-rounds 1` but does not explicitly disable Java compile repair; this checkout controls that separately with `--max-compile-repair-loops 0`. Do not present those archived commands as runnable against this implementation. `--no-test` alone also does not remove certification: with `--certify`, ephemeral tests can still be generated; the archived no-independent-tests arm uses both `--no-test` and `--no-certify`. Restoring the missing runner/version and full three-language artifacts is necessary for exact Table IV reproduction.

### RQ5: Human evaluation

The paper's procedure compares each sampled requirement's SRS text, inferred contract, and generated Dafny model using contract correctness, contract completeness, model faithfulness, and unsupported assumptions, followed by adjudication. The sample includes verified and unverified models. Reproduction needs the exact 50-item sample and source artifacts, both independent ratings, adjudication records, and agreement calculations. Those materials, including the previously referenced `Human_Evaluation_Cleanroom_agent.xlsx`, are absent from this checkout. The available [organized results workbook](results/organized_results.xlsx) is not a substitute for missing independent human ratings. The paper's reported counts above cannot be independently regenerated from the available ratings because those ratings are missing.

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
