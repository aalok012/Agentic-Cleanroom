# Full pipeline — run metrics across different models

_Auto-appended after every `run_pipeline.py` run. One section per run._

---

## Run 20260629-005628-foodsaver — FAILED

- **When**: 2026-06-28 19:56:28
- **SRS**: foodsaver.xml  ·  **language**: ?  ·  **stack**: auto
- **Command**: `python run_pipeline.py data/srs/foodsaver.xml --prove --certify --samples 1`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on, compile_repair=off
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 180,505 (in 153,776 / out 26,729) · calls 78
- estimated cost: $0.0444

- proved feature ids: (none)

---

## Run 20260629-033231-foodsaver — FAILED

- **When**: 2026-06-28 22:32:31
- **SRS**: foodsaver.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/foodsaver.xml --language python --stack fastapi --prove --certify --samples 1 --resume --output-dir outputs/foodsaver_lang/python`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on, compile_repair=off
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 543,019 (in 451,767 / out 91,252) · calls 147
- estimated cost: $0.1347

- proved feature ids: (none)

---

## Run 20260629-033254-foodsaver — FAILED

- **When**: 2026-06-28 22:32:54
- **SRS**: foodsaver.xml  ·  **language**: ?  ·  **stack**: spring
- **Command**: `python run_pipeline.py data/srs/foodsaver.xml --language java --stack spring --prove --certify --samples 1 --resume --output-dir outputs/foodsaver_lang/java`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on, compile_repair=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 0 (in 0 / out 0) · calls 0
- estimated cost: $0.0000

- proved feature ids: (none)

---

## Run 20260629-033316-foodsaver — FAILED

- **When**: 2026-06-28 22:33:16
- **SRS**: foodsaver.xml  ·  **language**: ?  ·  **stack**: express
- **Command**: `python run_pipeline.py data/srs/foodsaver.xml --language javascript --stack express --prove --certify --samples 1 --resume --output-dir outputs/foodsaver_lang/javascript`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on, compile_repair=off
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 0 (in 0 / out 0) · calls 0
- estimated cost: $0.0000

- proved feature ids: (none)

---

## Run 20260629-073733-foodsaver — COMPLETE

- **When**: 2026-06-29 02:37:33
- **SRS**: foodsaver.xml  ·  **language**: python  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/foodsaver.xml --language python --stack fastapi --prove --certify --samples 1 --resume --output-dir outputs/foodsaver_lang/python`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on, compile_repair=off
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

### Run metrics (summary)

| metric | value |
|---|---|
| PassVer@1 | 0.8919 |
| verification_pass_ratio | 0.8919 |
| test_case_pass_ratio | 0.0 |
| avg_verification_iteration | 2.38 |
| avg_test_iteration | 3 |
| avg_input_token | 3250.7 |
| avg_output_token | 840.6 |
| total_time (s) | 7179.0 |

#### Copy-paste row (TSV — paste directly under your spreadsheet header)

```text
verification_pass_ratio	test_case_pass_ratio	avg_input_token	avg_output_token	total_time	avg_verification_iter	avg_test_iter	PassVer@1
0.8919	0.0	3250.7	840.6	7179.0	2.38	3	0.8919
```

- tokens: 1,251,920 (in 994,707 / out 257,213) · calls 306
- estimated cost: $0.3159

### Dafny proof tier

- proved 28/37 features (rate 0.757)

| feature | result | rounds | axioms |
|---|---|---|---|
| 3.1.1 | PROVED | 1 | 0 |
| 3.1.10 | PROVED | 1 | 1 |
| 3.1.10_2 | PROVED | 1 | 0 |
| 3.1.11 | PROVED | 1 | 0 |
| 3.1.12 | unproved | 6 | 2 |
| 3.1.13 | PROVED | 1 | 0 |
| 3.1.14 | PROVED | 1 | 0 |
| 3.1.15 | PROVED | 1 | 0 |
| 3.1.16 | PROVED | 1 | 0 |
| 3.1.17 | unproved | 6 | 0 |
| 3.1.18 | PROVED | 1 | 0 |
| 3.1.19 | unproved | 6 | 0 |
| 3.1.2 | unproved | 6 | 0 |
| 3.1.20 | unproved | 6 | 0 |
| 3.1.21 | PROVED | 1 | 0 |
| 3.1.22 | PROVED | 1 | 0 |
| 3.1.23 | PROVED | 1 | 1 |
| 3.1.24 | PROVED | 1 | 1 |
| 3.1.25 | unproved | 6 | 0 |
| 3.1.26 | PROVED | 1 | 0 |
| 3.1.27 | PROVED | 1 | 0 |
| 3.1.28 | PROVED | 1 | 0 |
| 3.1.29 | PROVED | 1 | 0 |
| 3.1.3 | PROVED | 1 | 0 |
| 3.1.30 | PROVED | 1 | 0 |
| 3.1.31 | unproved | 6 | 0 |
| 3.1.32 | unproved | 6 | 0 |
| 3.1.33 | PROVED | 3 | 0 |
| 3.1.34 | PROVED | 1 | 0 |
| 3.1.35 | PROVED | 1 | 0 |
| 3.1.36 | unproved | 6 | 0 |
| 3.1.4 | PROVED | 2 | 1 |
| 3.1.5 | PROVED | 2 | 0 |
| 3.1.6 | PROVED | 1 | 0 |
| 3.1.7 | PROVED | 2 | 0 |
| 3.1.8 | PROVED | 1 | 0 |
| 3.1.9 | PROVED | 2 | 0 |

### Certification (pass@k)

- pass@1: 0.000
- case pass rate: 0.000
- pass@1 FR ids: (none)

### Recovery loops (full metrics per iteration)

| loop | targeted | reproved | still failing | pass@1 | PassVer@1 | case_pass | proved FRs | certified FRs |
|---|---|---|---|---|---|---|---|---|
| 1 | ['3.1.12', '3.1.17', '3.1.19', '3.1.2', '3.1.20', '3.1.25', '3.1.31', '3.1.32', '3.1.36'] | ['3.1.12', '3.1.2', '3.1.20', '3.1.32'] | ['3.1.17', '3.1.19', '3.1.25', '3.1.31', '3.1.36'] | 0.0 | 0.865 | 0.0 | 32/37 | 32/37 |
| 2 | ['3.1.17', '3.1.19', '3.1.25', '3.1.31', '3.1.36'] | ['3.1.19'] | ['3.1.17', '3.1.25', '3.1.31', '3.1.36'] | 0.0 | 0.892 | 0.0 | 33/37 | 33/37 |

- re-proved (now ship from Dafny): ['3.1.12', '3.1.19', '3.1.2', '3.1.20', '3.1.32']
- repaired-with-tests (clean-room relaxed): (none)
- still UNCERTIFIED: ['3.1.17', '3.1.25', '3.1.31', '3.1.36']

### Final per-feature outcome

| feature | outcome |
|---|---|
| 3.1.1 | PROVED |
| 3.1.10 | PROVED |
| 3.1.10_2 | PROVED |
| 3.1.11 | PROVED |
| 3.1.12 | PROVED (recovery) |
| 3.1.13 | PROVED |
| 3.1.14 | PROVED |
| 3.1.15 | PROVED |
| 3.1.16 | PROVED |
| 3.1.17 | UNCERTIFIED |
| 3.1.18 | PROVED |
| 3.1.19 | PROVED (recovery) |
| 3.1.2 | PROVED (recovery) |
| 3.1.20 | PROVED (recovery) |
| 3.1.21 | PROVED |
| 3.1.22 | PROVED |
| 3.1.23 | PROVED |
| 3.1.24 | PROVED |
| 3.1.25 | UNCERTIFIED |
| 3.1.26 | PROVED |
| 3.1.27 | PROVED |
| 3.1.28 | PROVED |
| 3.1.29 | PROVED |
| 3.1.3 | PROVED |
| 3.1.30 | PROVED |
| 3.1.31 | UNCERTIFIED |
| 3.1.32 | PROVED (recovery) |
| 3.1.33 | PROVED |
| 3.1.34 | PROVED |
| 3.1.35 | PROVED |
| 3.1.36 | UNCERTIFIED |
| 3.1.4 | PROVED |
| 3.1.5 | PROVED |
| 3.1.6 | PROVED |
| 3.1.7 | PROVED |
| 3.1.8 | PROVED |
| 3.1.9 | PROVED |

- proved feature ids: ['3.1.1', '3.1.10', '3.1.10_2', '3.1.11', '3.1.12', '3.1.13', '3.1.14', '3.1.15', '3.1.16', '3.1.18', '3.1.19', '3.1.2', '3.1.20', '3.1.21', '3.1.22', '3.1.23', '3.1.24', '3.1.26', '3.1.27', '3.1.28', '3.1.29', '3.1.3', '3.1.30', '3.1.32', '3.1.33', '3.1.34', '3.1.35', '3.1.4', '3.1.5', '3.1.6', '3.1.7', '3.1.8', '3.1.9']

---

## Run 20260628-101510-human — COMPLETE

- **When**: 2026-06-28 05:15:10
- **SRS**: Human.xml  ·  **language**: python  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/Human.xml --prompt-strategy cot --model deepseek/deepseek-v3.2 --no-prove --no-certify --output-dir outputs/smoke_cot`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=off, code=on, test=on, certify=off, recovery=off, compile_repair=off
- certify=False · samples=1 · k=[1] · prove=False · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

### Run metrics (summary)

| metric | value |
|---|---|
| PassVer@1 | 0.0 |
| verification_pass_ratio | 0.0 |
| test_case_pass_ratio | 0.0 |
| avg_verification_iteration | 0.0 |
| avg_test_iteration | 0.0 |
| avg_input_token | 1909.1 |
| avg_output_token | 861.2 |
| total_time (s) | 188.57 |

#### Copy-paste row (TSV — paste directly under your spreadsheet header)

```text
verification_pass_ratio	test_case_pass_ratio	avg_input_token	avg_output_token	total_time	avg_verification_iter	avg_test_iter	PassVer@1
0.0	0.0	1909.1	861.2	188.57	0.0	0.0	0.0
```

- tokens: 22,163 (in 15,273 / out 6,890) · calls 8
- estimated cost: $0.0059

---

## Run 20260629-094017-foodsaver — FAILED

- **When**: 2026-06-29 04:40:17
- **SRS**: foodsaver.xml  ·  **language**: java  ·  **stack**: spring
- **Command**: `python run_pipeline.py data/srs/foodsaver.xml --language java --stack spring --prove --certify --samples 1 --resume --output-dir outputs/foodsaver_lang/java`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-v3.2` |
| dependency | `deepseek/deepseek-v3.2` |
| planning | `deepseek/deepseek-v3.2` |
| code | `deepseek/deepseek-v3.2` |
| test | `deepseek/deepseek-v3.2` |
| proof | `deepseek/deepseek-v3.2` |
| cert | `deepseek/deepseek-v3.2` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on, compile_repair=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=2 · max_compile_repair_loops=2
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 1,243,223 (in 1,017,933 / out 225,290) · calls 305
- estimated cost: $0.3102

- proved feature ids: (none)

