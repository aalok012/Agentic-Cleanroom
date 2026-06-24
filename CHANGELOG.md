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

## 2026-06-24 — Headline run-metrics are all FR-level now

### Changed
- **`_compute_summary` reports every ratio at FR granularity** (the FR is the atomic
  independently-certifiable unit; the per-FR pass@k already used it, but proof/PassVer were
  feature-level, so the headline numbers mixed denominators). How: `verification_pass_ratio` =
  |FRs of proved features| / total FRs; `PassVer@1` = |FRs of proved features ∪ FRs passing pass@1|
  / total FRs (a proved feature certifies ALL its FRs; union dedupes overlap);
  `avg_verification_iteration` is FR-weighted (each FR inherits its feature's proof rounds).
  Certification now stores `pass_at_1_fr_ids` (from `cert.frs`) instead of feature ids. Tests
  rewritten to FR-level synthetic data; suite 66 passed.

## 2026-06-24 — Drop the redundant `<stem>_ir.json` dump from pipeline runs

### Changed
- **`SpecAgent.run` writes `_ir.json` only when `output_dir` is given.** Why: the per-stage spec
  dump is a strict SUBSET of the final `full_ir.json` (each stage writes the whole running IR, so
  ir ⊂ contracts ⊂ dependency ⊂ planning ⊂ full_ir) — pure duplication in a full run. How:
  `output_dir: Path | None`; `run_pipeline` Stage 1 now passes `output_dir=None`. Standalone
  `spec_agent/cli.py` still writes it. Suite: 66 passed.

## 2026-06-24 — Cross-agent audit: de-bias schemas/prompts for python | fastapi | java

Read every agent's schema + prompt and made them correct/parameterized for all three targets.
Most were already target-agnostic (spec contract is explicitly stack-agnostic; dependency is
language-neutral; code + test prompts dispatch via the language target; certification/dafny
schemas are neutral). Two real biases fixed:

### Changed
- **Planning had no Java branch.** Why: `plan_feature.j2`'s TARGET STACK was `fastapi` vs
  `else=plain Python`, so a `--language java` run (stack="java") was told "plain Python". How:
  added a `java` branch, and reframed the signature as the CANONICAL language-neutral interface
  (Python syntax) that codegen realizes in the target language — updated `FRPlan.signature` /
  `Contract.signature` descriptions to match.
- **Test schema was Python-named.** Why: `FeatureTests.pytest_source` held the JUnit class on a
  Java run, and `expected_json`'s description hardcoded `ValueError`. How: renamed
  `pytest_source → test_source` (all refs in `test/agent.py` + both test prompts), generalized its
  description (pytest for Python/FastAPI, JUnit5 for Java), and generalized the `raises` example to
  name the per-target exception. Suite: 66 passed.

### Changed
- **`infer_fr_deps.j2` sharpened.** Why: the most error-prone rule ("a cross-reference is not a
  dependency") was only described, never shown, inviting false-positive edges. How: added a worked
  NEGATIVE example beside the positive one, and reworded the DIRECTION block from "source/target"
  to the actual structured-output field names (`id` / `prerequisite_ids`) so the model fills the
  schema directly. No code change; suite still 66 passed.

## 2026-06-24 — Code-agent prompts: de-bias across stacks (Python/Java parity)

### Changed
- **Java codegen prompt brought to parity with Python.** Why: `generate_code_java.j2` was thinner
  than `generate_code.j2`, making Java a second-class citizen. How: added the same
  contract-adherence framing ("implement EXACTLY this contract, nothing beyond it"), full
  prerequisites guidance (don't call update/setup from read paths), exact-output matching, and
  direct-map-key reading — Java-correct equivalents of the Python rules.
- **All code-agent templates now route through the target.** Why: `generate_adapter.j2` and
  `regenerate_with_feedback.j2` were hardcoded in `code/agent.py`, i.e. silently Python-only — a
  latent bias if ever run for Java. How: `LanguageTarget.adapter_template()` /
  `feedback_template()` (base returns the Python prompts); `JavaTarget` overrides them to raise
  `NotImplementedError` (adapter = FastAPI-only, recovery = Python-only in v1) so nothing silently
  falls back to a Python prompt. `code/agent.py` renders via `self.target.*`.
- Tests: target routing + Java-refusal + Java-prompt parity (prereqs/error-mode). Suite: 66 passed.

## 2026-06-24 — Configurable, multi-language pipeline (Python + Java) via CLI

Make the pipeline versatile: choose the target **language** (python | java) and configure
**every knob via the CLI** — a separate model per stage, pass@k, samples, stack, prove/certify.
Java produces Java code + JUnit tests and (with a JDK) compile-checks them. Built in three
phases behind a clean target abstraction so the Python path is unchanged.

### Added
- **Step 1 — `RunConfig` (`src/cleanroom/config.py`).** Why: one object holding every knob,
  populated from argparse, threaded through `run()`. How: dataclass with per-stage models
  (`spec/dependency/planning/code/test/proof/cert`), `language`, `stack`, `samples`, `k_values`,
  prove/certify; `from_args()` (java pins its own stack; `--prove-target` follows the language).
- **Step 2 — Per-stage model selection.** Why: a mixed-model run (e.g. cheap spec, strong code)
  prices correctly via the existing `estimate_cost_by_model`. How: `run()` builds a separate
  `get_llm(model=...)` per agent instead of one shared client; new flags `--spec-model …
  --cert-model`, plus `--language`, `--k`.
- **Step 3 — `LanguageTarget` abstraction (`src/cleanroom/targets/`).** Why: keep all
  language-specific choices (templates, packaging, oracle) in one place. How: base class *is* the
  Python behavior; `JavaTarget` overrides. `CodeAgent`/`TestAgent`/`CertificationAgent` take a
  `language` and dispatch the codegen/test template and the oracle through `self.target` instead
  of branching on `stack` inline (Python output unchanged).
- **Step 4 — Java target.** Why: the new capability. How: `targets/java.py`; prompts
  `generate_code_java.j2` (plain Java class per contract, stdlib only) + `generate_tests_junit.j2`
  (JUnit5); `utils/java_packager.py` (write `<PublicClass>.java`); `utils/java_tooling.py`
  (`java_available`/`junit_jar` — mirrors `dafny_available`); `run_case_java` in
  `evaluation/runner.py` (v1 oracle = `javac` compile-check; full JUnit execution deferred behind
  `$JUNIT_JAR`). Certification skips gracefully when no JDK; recovery loop stays Python-only.

- **Step 5 — Headline run-metrics summary.** Why: surface the research metrics in one organized
  block at the end of every run (and in the run report). How: `_compute_summary` + `_print_summary`
  in `run_pipeline.py` emit `verification_pass_ratio`, `test_case_pass_ratio`, `PassVer@1`
  (= (proved + pass@1) / total features), `avg_verification_iteration` (mean Dafny rounds),
  `avg_test_iteration` (1 + recovery passes), `avg_input_token`, `avg_output_token`, `total_time`.

- **Step 6 — `PassVer@1` is a set UNION, not a sum.** Why: `PassVer@1` = features certified by
  proof OR pass@1, over all features. The first cut summed `n_proved + n_pass@1`, which
  double-counts a feature that is both proved and passes pass@1 (possible when proved features
  aren't skipped from the test track — non-adapter stacks) and can exceed 1.0. How: thread the
  proved feature ids + pass@1 feature ids into the summary and compute `|proved ∪ pass@1| / total`.

### Tests
- **Step 7 — `tests/test_config.py`, `tests/test_targets.py`, `tests/test_summary.py`.** Config
  mapping, registry, Python template parity, Java prompt render, java packaging, a `javac`
  compile-oracle test (`skipif(not java_available())`), the summary metric definitions, and a
  PassVer@1 union/dedup test. Full suite: 64 passed.

### Non-goals (v1)
- Java web framework (Spring), a Java Dafny-core adapter, and executing the generated JUnit per
  case (needs a JUnit jar + JSON marshalling) are follow-ups.

## 2026-06-24 — Default certification to pass@1 only; finish dead `revise()` removal

### Changed
- **Step 1 — pass@1 is the only default metric.** Why: generating 3 samples just to
  compute pass@3 burns 3× the tokens, and the pipeline standardized on pass@1 (the
  recovery loop already uses it). How: `CertificationAgent.k_values` defaults to
  `[1]` (was `[1, 3] if n >= 3`); `--samples` default `3 → 1` and `run()` default
  `5 → 1`. Multi-sample estimates still possible via explicit `k_values`/`--samples`.

### Removed
- **Step 2 — Deleted the orphaned `revise()` path.** Why: commit a6d0ca0 removed
  `generate_code_revision.j2` but left `CodeAgent.revise()` + its test referencing the
  now-missing template (the suite's only failure). `revise()` had zero callers since the
  verify→revise loop was dropped. How: removed `revise()` from `code/agent.py` and
  `test_generate_code_revision_j2` from `tests/test_template_alignment.py`. Suite: 48 passed.

## 2026-06-24 — Recovery loop (re-prove + test-informed regen) at Stage 4↔6

Adds a last-resort fallback so a feature that fails BOTH formal proof and the
clean-room pass@1 gets one more chance: re-prove it harder, and if it still won't
verify, regenerate its code WITH the failing test cases fed back, then re-certify.
User decisions for this loop: full test feedback (deliberate, contained clean-room
break), configurable cap (`--max-cert-loops`, default 2), and both escalations
(Dafny rounds + code temperature). Failing signal = pass@1 < 1.0.

### Added
- **Step 1 — `CertificationResult.failures`.** Why: the loop needs the failing
  inputs/expected/reason to feed back. How: added the field in
  `src/cleanroom/agents/evaluation/schema/certification.py` and populated it in
  `certify()` (`agents/evaluation/agent.py`) from the existing diagnostics.
- **Step 2 — Test-informed repair prompt.** Why: a regeneration prompt that
  shows the failing cases (the clean-room first pass must NOT). How: new
  `src/cleanroom/agents/code/prompts/regenerate_with_feedback.j2`.
- **Step 3 — `CodeAgent.regenerate_with_test_feedback(...)`.** Why: the ONLY code
  path that may see tests; the clean `generate()` stays untouched. How: new method
  in `agents/code/agent.py` with a loud header marking the contained clean-room
  break; regenerates only the targeted failing features, embedding each FR's
  failing cases.
- **Step 4 — `RecoveryLoop`.** Why: orchestrate (a) escalated re-prove → ship as
  Dafny-core adapter, (b) test-informed regen, (c) re-certify (n=1, pass@1), up to
  the cap. How: new `src/cleanroom/agents/recovery/loop.py` (+ `__init__.py`).
  Escalation: Dafny rounds `6 + 2·i`, code temperature `0.4 + 0.2·i`. Tests are
  NEVER regenerated inside the loop (the oracle stays frozen).
- **Step 5 — Per-feature certification labels.** Why: never overclaim a clean-room
  pass we didn't earn. How: the loop emits `PROVED` / `TESTED (clean-room)` /
  `TESTED (repaired-with-tests)` / `UNCERTIFIED`, surfaced in the run report.

### Changed
- **Step 6 — Wired the loop into `run_pipeline.py`.** Why: run it after Stage 6.
  How: new `--max-cert-loops` flag (default 2; needs `--certify`; 0 disables);
  Stage 6b invokes `RecoveryLoop`, swaps the repaired result/code into the IR and
  metrics, and prints the labels. Added a "Recovery loop" section to the run report.

### Tests
- **Step 7 — `tests/test_recovery_loop.py`.** Why: lock the deterministic
  orchestration offline. How: fake LLM + stubbed `_certify` covering the
  test-informed regen targeting, the pass@1 failing signal, repair→label, and the
  give-up→UNCERTIFIED + escalation schedule. Full suite: 49 passed.

---

## 2026-06-23 — Stronger MVC-classification prompt; drop the keyword fallback

### Changed — `plan_feature.j2` MVC classifier
Rewrote the `mvc_layer` instruction with a Role/Definitions/Data-flow/Example structure: classify
from the behavioral **contract** (stimulus + response), not name keywords; strict separation-of-
concerns definitions for model/view/controller; a data-flow line (Controller → Model → View);
a primary-effect tie-breaker (state change → controller even if it also reads; pure read → view;
bare entity store → model); and three worked examples. Made the FastAPI `TARGET STACK` block map
each layer to a concrete artifact (model=SQLAlchemy, controller=APIRouter handler, view=read
endpoint/serializer). This fixes mis-tags like 4.1 ("Place Order" — a create) being labelled `view`.

### Removed — the deterministic keyword classifier
`MVC_KEYWORDS` + `classify_layer` deleted (the prompt is now the sole classifier; the Literal-typed
`mvc_layer` field already constrains output). `_normalize_layer` now just defaults invalid output to
`controller`. Restored `_LAYER_DIR` (the model→models/ directory map — not a classifier, still used
for file paths). Fixed the resulting `NameError`. Suite **45 passed**.

---

## 2026-06-23 — Remove the LLM Verification Agent entirely

The LLM "Verification Agent" was a reasoning-only reviewer (not a real verifier). Removed it so the
pipeline has one honest verification story: the Dafny proof track. Code is now generated and either
proved (Dafny) or tested (pass@k) — no LLM "review" middle layer.

### Removed
- Deleted `src/cleanroom/agents/verification/` (agent.py, loop.py, schema, `verify_contract.j2`).
- `run_pipeline.py`: dropped `--verify`/`--verify-rounds`/`--verify-model`/`--verify-passes`, the
  Stage 4b block, the `verification` metrics + report section, and the `generate_and_verify` path
  (code is now just `code_agent.generate` or the adapter split).
- `CertificationAgent`: dropped `verify*` params, the `VerificationAgent`/`generate_and_verify`
  imports, and the verify branch in `_collect_samples`.
- Removed the stale `test_verify_contract_j2` template test.
- README/diagrams/flags + `run_record.py` de-referenced the agent; `run_record` now persists the
  `dafny`/`compile` metrics (and a Dafny proof-tier section) instead of `verification`.

Suite **45 passed**. Pipeline stages are now: Spec → Dependency → Planning → [4a Prove] → Code →
Test → [6 Certify].

---

## 2026-06-23 — De-brand: remove the "lemmafit" name from submitted artifacts

For the research submission: strip the literal name "lemmafit" from `src/`, `README.md`, `docs/`
(dev logs CHANGELOG/RUN_RESULTS kept as honest history). **Labels/comments/filenames only — no
technical content changed**, so the proof pipeline behaves identically (system prompt 6931→6891
chars: only headings differ; the Dafny examples, proof tactics, kernel code, and contracts are
byte-identical). Renamed `skills/lemmafit-{dafny,proofs}.md` → `skills/dafny-{patterns,proofs}.md`
(updated `_load_skill` args + the `=== DAFNY PATTERNS/PROOFS ===` prompt headers); de-branded
docstrings/comments in `agent.py`, `dafny_verify.py`, `dafny_project.py`, `kernel/Replay.dfy`,
tests, docs, README; removed the dead `~/.lemmafit` binary-probe fallback (PATH is checked first, so
behaviour is unchanged). Suite 46.

NOTE (provenance): the `Replay.dfy` kernel and the two `skills/` guidance docs are *adapted from
LemmaFit (MIT)*. The in-code attribution was removed per request, but the derivation should be
acknowledged in the paper — renaming does not make the work original.

---

## 2026-06-23 — Real (vendored) LemmaFit prompts, drop SPEC.yaml, verification-workflow doc

### Fixed — proof-prompt regression
- A previous edit had bloated the global proof prompt (`PROOF_REF`), which **regressed the proof
  count 6→4** in a full run (broke 4.4/4.5/4.8/4.9, several into syntax errors). Root cause:
  wall-specific tactics in the *system* prompt hurt the easy cases.
- Now use the **actual LemmaFit skill prompts verbatim**, vendored in-repo at
  `src/cleanroom/agents/dafny/skills/{lemmafit-dafny,lemmafit-proofs}.md` (the tuned originals that
  achieved 6/10), instead of a hand-condensed paraphrase. `DafnyAgent._build_system` loads them;
  `DAFNY_REF` syntax guardrails kept; wall-specific tactics live ONLY in `_targeted_hint` (fired on
  the matching error during revise). No runtime LemmaFit dependency — the skill text is owned in-repo.

### Removed — SPEC.yaml conversion (vestigial)
- Verification reads the `.dfy` directly; nothing consumed `SPEC.yaml` (no LemmaFit daemon/claimcheck).
  Deleted `utils/dafny_spec.py` + `tests/test_dafny_spec.py`; dropped `GeneratedDafny.spec_yaml`, the
  `proj/SPEC.yaml` write, and the redundant spec-entries section in the Dafny prompt (postconditions
  still flow via the behavioral contracts).

### Added
- `docs/dafny-verification-workflow.md` — full workflow: the inner mechanism (Dafny→Boogie→VCs→Z3,
  proof by refutation, inductive invariant safety), the proof walls, and the DafnyAgent
  generate→verify→revise→compile loop, with diagrams.

Suite **46 passed** (−4 = the removed SPEC.yaml tests).

---

## 2026-06-22 — Fix adapter app-boot failures found by the first real --prove run

The first paid `--prove --certify` FastAPI run (6/10 proved, $0.62, logged correctly with the new
mixed-model cost) failed every pass@k test with `ModuleNotFoundError: No module named
'dafny_marshal'`. Two bugs, both diagnosed + fixed + validated for $0 (n=1 pipeline sample, no LLM):

### Fixed
- **Cert oracle didn't stage the Dafny cores.** `CertificationAgent._write_sample` re-packages each
  sample into a temp app but never copied `dafny_cores/` → proved-feature adapters' `import
  dafny_marshal` crashed at boot → ALL tests failed (even unproved features). Fix: `_write_sample`
  now calls `stage_dafny_cores`; `__init__` takes `dafny_proj`/`dafny_modules`; `run_pipeline` passes
  them when `adapter_mode`.
- **Dafny mangles `_`→`__` in compiled module names.** Adapter imported `F4_1Domain` but Dafny emits
  `F4__1Domain.py` — earlier tests missed it (underscore-free names `Menu`/`Fm`). Fix:
  `generate_adapter` mangles `core_module = f"{module}Domain".replace("_","__")` (the core DIR keeps
  the single underscore). Regression test now uses an underscored module.
- **pytest scoped to `tests/`** (`pyproject.toml [tool.pytest.ini_options] testpaths`) so generated
  test artifacts under `outputs/` no longer pollute the suite.

### Validated (free, n=1 local re-cert with both fixes)
- App boots; all 6 proved adapters import (no `module_`/`_dafny` multi-core collision). Unproved
  features now test for real: 4.3=1.00 (4/4), 4.10=2/4, 4.6=2/4, 4.7=1/3 → aggregate pass@1 **0.25**,
  case rate **0.60** (was 0.00 / all-boot-crash). Remaining failures are genuine code issues
  (empty-DB seeding, validation) — what pass@k should catch. Suite **50 passed**.

---

## 2026-06-21 — Accurate per-model API-usage cost (mixed-model --prove runs)

Goal: a `--prove` run mixes models (gpt-4o-mini for most stages + gpt-4.1 for the proof tier), but
the usage log priced ALL tokens at the last model's rate — under-billing the expensive gpt-4.1
tokens ~9× (a real $0.37 run logged as $0.04). Token COUNTS were always accurate; only the dollar
figure was wrong.

### Added / Changed
- **`estimate_cost_by_model(calls)`** in `cost.py` — groups the per-call records (model already
  recorded in `GLOBAL_METRICS.calls`) by model and prices each at its own rate. Tests: `test_cost.py`.
- **`_finalize_metrics` + `metrics_from_globals`** now use it: `cost_usd` is the exact per-model sum,
  `model` shows all models used (e.g. `gpt-4.1+gpt-4o-mini`), and `cost_by_model` is stored.
- **Run report** prints a per-model cost breakdown for mixed runs.
- Logging path unchanged and confirmed: `append_usage_log` writes to `API_USAGE.md` on BOTH success
  and failure (partial runs still counted), with cumulative totals + per-run history. Suite **50**.

---

## 2026-06-21 — Ship the PROVED logic from Dafny (FastAPI core + thin adapter)

Goal (user decision): for a FastAPI feature that the proof tier verifies, **ship the logic as the
compiled Dafny core** rather than CodeAgent-generated code — the Code Agent writes only the thin
DB/HTTP adapter that calls the proved core. Unproved features fall back to full CodeAgent code +
pass@k (prove-or-test). Reorders the pipeline so the proof tier runs BEFORE codegen.

### De-risked first (free, no LLM)
- Confirmed `dafny translate py` output is callable: `MenuDomain.default__.Apply/Normalize`,
  `Action_*` constructors, `_dafny` runtime bundled in `<module>-py/`. Inputs/outputs are Dafny
  runtime types (`_dafny.Seq` strings via `VerbatimString(False)`, `_dafny.Map` state). Validated a
  full JSON round-trip through a compiled core.

### Added
- **`src/cleanroom/utils/dafny_marshal.py`** — JSON/DB ↔ Dafny-runtime shim (`to_str/from_str`,
  `to_seq/from_seq`, `to_map/from_map`), shipped INTO the app so adapters import it. Lazy `_dafny`
  import so it loads anywhere. Tests: `tests/test_dafny_marshal.py` (incl. a real compile+roundtrip).
- **`CodeAgent.generate_adapter`** + **`generate_adapter.j2`** — writes one FastAPI controller per
  proved feature that imports the compiled core, persists the Dafny Model as serialized state,
  marshals via `dafny_marshal`, and calls `Normalize(Apply(state, action))` — NO business logic.
  Prompt bakes in the validated calling convention + an upward `dafny_cores` discovery header.
- **`CodeAgent.generate(skip_feature_ids=…)`** — omit whole features (those shipping from Dafny).
- **`stage_dafny_cores`** (`dafny_project.py`) — copy each proved `out/<mod>-py/` + the shim into
  `app/dafny_cores/`. Tests: `tests/test_adapter_mode.py`.

### Changed
- **`run_pipeline.py` reorder**: proof tier is now **Stage 4a (before codegen)**. `adapter_mode =
  prove and stack==fastapi and proved>0`: proved features → `generate_adapter` over the compiled
  core; the rest → `generate(skip_feature_ids=proved)`; app packaging stages the cores+shim. pass@k
  skips proved features only in adapter_mode (`cert_skip`). On the python stack `--prove` stays
  proof-only (code/test proceed for all). `--verify` applies only on the non-adapter path.

### Verified
- Full suite **46 passed**. Offline-validated: adapter file placement + prompt conventions, feature
  skipping, core/shim staging, and (with real dafny) the compiled-core round-trip. NOTE: adapter
  *quality* (does the LLM write correct glue for arbitrary Model shapes) is unproven until a real
  `--prove --certify` FastAPI run — that's the paid validation step.

---

## 2026-06-21 — De-LemmaFit + prove-or-test certification tiering

Goal (user decision): drop the LemmaFit runtime dependency (it's a wrapper of Dafny + workflow +
prompts — we already call `dafny verify` directly), and restructure the pipeline so `lemmafit` is
no longer a stack. New shape: generate the MVC app in the best stack, then per feature **prove**
its logic in Dafny where possible (compile proved features to native code) and **test** the rest
with the Testing Agent (pass@k) — a prove-or-test fallback.

### Removed
- **LemmaFit runtime dependency.** Why: the verifier was always just `dafny verify` + a parse; the
  CLI/daemon/dafny2js/npm/`.claude/skills` were workflow, not verification. How: deleted
  `src/cleanroom/utils/lemmafit_project.py` (lemmafit init + npm + dafny2js compile) and the stale
  `scripts/lemmafit_dafny_spike.py`; dropped `--stack lemmafit`.

### Added
- **Vendored kernel** `src/cleanroom/agents/dafny/kernel/Replay.dfy`. Why: own the abstract
  Domain/Kernel features refine, instead of getting it from `lemmafit init`.
- **`src/cleanroom/utils/dafny_project.py`** — `scaffold_dafny_project` (mkdir + copy vendored
  kernel, no CLI/npm) and `compile_dafny` (`dafny translate <target>`, default `py`, replaces
  dafny2js).
- **`extract_axioms`** in `dafny_verify.py` — surfaces `assume {:axiom}` escape hatches
  (`DafnyResult.axioms`), so an unprovable obligation can pass as an explicit, auditable assumption.
- **Proof tier (`--prove`)** + **`--prove-target`** in `run_pipeline.py`: Stage 5b authors+proves a
  Dafny state machine per feature (gpt-4.1), compiles proved features to native code, degrades
  gracefully (no dafny binary → 0 proved → everything tested).
- **`skip_feature_ids`** on `CertificationAgent`: pass@k skips features already PROVED by the tier
  (the test-fallback half of prove-or-test).

### Changed
- **`DafnyAgent`** (`agents/dafny/agent.py`): reads the vendored kernel from `<proj>/dafny/`; prompt
  knowledge owned in-repo (`DAFNY_REF` syntax + new `PROOF_REF` tactics folded in from the former
  LemmaFit skills); no `.claude/skills` reads. System prompt de-branded from "LemmaFit".
- **Renamed** `utils/lemmafit_spec.py` → `utils/dafny_spec.py`; `tests/test_lemmafit_spec.py` →
  `tests/test_dafny_spec.py`.
- **`dafny_verify.py`** binary probe: $DAFNY → PATH → `~/.lemmafit` download (now just a fallback,
  not a requirement).
- **`run_pipeline.py`** flow: removed the `if stack == "lemmafit": … return` branch; `--stack`
  restricted to `auto|python|fastapi`; run-report headings de-branded (proof tier / native compile).

### Verified
- Imports resolve; offline scaffold copies the 155-line kernel; CLI exposes `--prove`/`--prove-target`
  and `--stack {auto,python,fastapi}`. Full suite **41 passed**.

### Fixed (two-pass review against the agreed pipeline)
- **Axiom audit trail propagated.** Why: `extract_axioms` existed but nothing carried `assume {:axiom}`
  through, so a feature passing via an assumed axiom was silently labeled PROVED. How: added
  `FeatureDafny.axioms` (+ `proved_clean` property); `DafnyAgent` populates it from `res.axioms`;
  run output / `metrics['dafny']` / run-report now show "PROVED [N assumed axiom(s)]" and a
  `n_proved_with_axioms` count.
- **All-proved certification reporting.** Why: when every feature was proved, pass@k had nothing to
  test and printed a misleading `pass@1: 0.000`. How: print "(no features to test — all certified by
  the proof tier)" when `cert.frs` is empty; otherwise annotate pass@k with the un-proved FR count;
  added `n_tested_frs`/`n_proved_features` to metrics.
- **Validated against a real Dafny binary** (Homebrew dafny 4.11 on PATH, after removing the LemmaFit
  toolchain): end-to-end scaffold(vendored kernel)+`verify_dafny` of a refining module (3 verified, 0
  errors); `compile_dafny` real `dafny translate py` → `out/<mod>-py`; axiom escape-hatch verifies and
  is recorded. Full suite **41 passed**.

### Ops (LemmaFit removal from the machine)
- Removed `~/lemmafit` scratch project (stale daemon status panel), the global `lemmafit` npm package
  (+bin symlink), and `~/.lemmafit/.dafny2js`. Installed `dafny` independently (`brew install dafny`,
  4.11 on PATH) and removed `~/.lemmafit` entirely. Cleared the stale LemmaFit block from
  `~/.claude/CLAUDE.md`. The pipeline's verifier now finds dafny on PATH.

---

## 2026-06-21 — Remove the python-stack deterministic verification layers

Goal (user decision): with verification moving to the LemmaFit/Dafny track, strip the two
deterministic verdict sources from the python-stack generate→verify→revise loop. Verdicts now
come solely from the LLM `VerificationAgent`; the `verifier=None` path is a no-op pass-through.

### Removed
- **CrossHair symbolic verifier.** Why: deterministic layer no longer wanted on the python
  track. How: `git rm src/cleanroom/agents/verification/crosshair_verify.py` +
  `tests/test_crosshair_verify.py`.
- **Executable canonical-I/O oracle.** Why: the other deterministic source, removed together.
  How: `git rm src/cleanroom/agents/verification/executable.py` (`executable_verdicts`,
  `merge_verdicts`).

### Changed
- **`loop.py` `generate_and_verify`.** Why: drop the two deterministic groups. How: `_verdicts`
  now returns `{}` when `verifier is None`, else the LLM verdicts only; removed crosshair/
  executable imports; aggregate model label `deterministic`→`none`; updated docstrings.
- **`run_pipeline.py`.** Why: the `elif certify and stack == "python"` deterministic-fix branch
  had no verdict source left. How: removed it (and the `crosshair_available` print) so python
  `--certify` falls through to plain `code_agent.generate`.
- **`evaluation/agent.py`.** Why: same — the python per-sample `generate_and_verify(max_rounds=2)`
  branch is now equivalent to plain generate. How: collapsed it into the `else` branch.

### Verified
- Imports resolve (`run_pipeline`, loop, `CertificationAgent`); no dangling refs to removed
  symbols. Full suite **41 passed** (down from 47 — the 6 removed crosshair tests).

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
