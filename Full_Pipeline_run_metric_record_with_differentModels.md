# Full pipeline — run metrics across different models

_Auto-appended after every `run_pipeline.py` run. One section per run._

---

## Run 20260625-075012-dineout-srs — FAILED

- **When**: 2026-06-25 02:50:12
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model openai/gpt-oss-120b --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `openai/gpt-oss-120b` |
| dependency | `openai/gpt-oss-120b` |
| planning | `openai/gpt-oss-120b` |
| code | `openai/gpt-oss-120b` |
| test | `openai/gpt-oss-120b` |
| proof | `openai/gpt-oss-120b` |
| cert | `openai/gpt-oss-120b` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 4,288 (in 1,755 / out 2,533) · calls 2
- estimated cost: $0.0018

- proved feature ids: (none)

---

## Run 20260625-083356-dineout-srs — COMPLETE

- **When**: 2026-06-25 03:33:56
- **SRS**: dineout_srs.xml  ·  **language**: python  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model anthropic/claude-sonnet-4-6 --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `anthropic/claude-sonnet-4-6` |
| dependency | `anthropic/claude-sonnet-4-6` |
| planning | `anthropic/claude-sonnet-4-6` |
| code | `anthropic/claude-sonnet-4-6` |
| test | `anthropic/claude-sonnet-4-6` |
| proof | `anthropic/claude-sonnet-4-6` |
| cert | `anthropic/claude-sonnet-4-6` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

### Run metrics (summary)

| metric | value |
|---|---|
| PassVer@1 | 1.0 |
| verification_pass_ratio | 0.9615 |
| test_case_pass_ratio | 1.0 |
| avg_verification_iteration | 1.96 |
| avg_test_iteration | 1 |
| avg_input_token | 3549.6 |
| avg_output_token | 1718.1 |
| total_time (s) | 1541.04 |

#### Copy-paste row (TSV — paste directly under your spreadsheet header)

```text
verification_pass_ratio	test_case_pass_ratio	avg_input_token	avg_output_token	total_time	avg_verification_iter	avg_test_iter	PassVer@1
0.9615	1.0	3549.6	1718.1	1541.04	1.96	1	1.0
```

- tokens: 363,474 (in 244,922 / out 118,552) · calls 69
- estimated cost: $0.1079

### Dafny proof tier

- proved 9/10 features (rate 0.9)

| feature | result | rounds | axioms |
|---|---|---|---|
| 4.1 | PROVED | 3 | 1 |
| 4.10 | PROVED | 2 | 0 |
| 4.2 | PROVED | 1 | 0 |
| 4.3 | unproved | 6 | 0 |
| 4.4 | PROVED | 1 | 0 |
| 4.5 | PROVED | 1 | 0 |
| 4.6 | PROVED | 1 | 0 |
| 4.7 | PROVED | 1 | 0 |
| 4.8 | PROVED | 2 | 0 |
| 4.9 | PROVED | 2 | 0 |

### Certification (pass@k)

- pass@1: 1.000
- case pass rate: 1.000
- pass@1 FR ids: ['4.3.REQ-1']

### Final per-feature outcome

| feature | outcome |
|---|---|
| 4.1 | PROVED |
| 4.10 | PROVED |
| 4.2 | PROVED |
| 4.4 | PROVED |
| 4.5 | PROVED |
| 4.6 | PROVED |
| 4.7 | PROVED |
| 4.8 | PROVED |
| 4.9 | PROVED |

- proved feature ids: ['4.1', '4.10', '4.2', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9']

---

## Run 20260625-090017-dineout-srs — FAILED

- **When**: 2026-06-25 04:00:17
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model deepseek/deepseek-chat --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-chat` |
| dependency | `deepseek/deepseek-chat` |
| planning | `deepseek/deepseek-chat` |
| code | `deepseek/deepseek-chat` |
| test | `deepseek/deepseek-chat` |
| proof | `deepseek/deepseek-chat` |
| cert | `deepseek/deepseek-chat` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 1,953 (in 1,118 / out 835) · calls 1
- estimated cost: $0.0007

- proved feature ids: (none)

---

## Run 20260625-090505-dineout-srs — FAILED

- **When**: 2026-06-25 04:05:05
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model deepseek/deepseek-chat --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-chat` |
| dependency | `deepseek/deepseek-chat` |
| planning | `deepseek/deepseek-chat` |
| code | `deepseek/deepseek-chat` |
| test | `deepseek/deepseek-chat` |
| proof | `deepseek/deepseek-chat` |
| cert | `deepseek/deepseek-chat` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 0 (in 0 / out 0) · calls 0
- estimated cost: $0.0000

- proved feature ids: (none)

---

## Run 20260625-090529-dineout-srs — FAILED

- **When**: 2026-06-25 04:05:29
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model deepseek/deepseek-chat --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-chat` |
| dependency | `deepseek/deepseek-chat` |
| planning | `deepseek/deepseek-chat` |
| code | `deepseek/deepseek-chat` |
| test | `deepseek/deepseek-chat` |
| proof | `deepseek/deepseek-chat` |
| cert | `deepseek/deepseek-chat` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 0 (in 0 / out 0) · calls 0
- estimated cost: $0.0000

- proved feature ids: (none)

---

## Run 20260625-091354-dineout-srs — FAILED

- **When**: 2026-06-25 04:13:54
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model deepseek/deepseek-chat --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-chat` |
| dependency | `deepseek/deepseek-chat` |
| planning | `deepseek/deepseek-chat` |
| code | `deepseek/deepseek-chat` |
| test | `deepseek/deepseek-chat` |
| proof | `deepseek/deepseek-chat` |
| cert | `deepseek/deepseek-chat` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 17,049 (in 13,824 / out 3,225) · calls 12
- estimated cost: $0.0040

- proved feature ids: (none)

---

## Run 20260625-091755-dineout-srs — FAILED

- **When**: 2026-06-25 04:17:55
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model deepseek/deepseek-chat --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-chat` |
| dependency | `deepseek/deepseek-chat` |
| planning | `deepseek/deepseek-chat` |
| code | `deepseek/deepseek-chat` |
| test | `deepseek/deepseek-chat` |
| proof | `deepseek/deepseek-chat` |
| cert | `deepseek/deepseek-chat` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 13,160 (in 10,605 / out 2,555) · calls 9
- estimated cost: $0.0031

- proved feature ids: (none)

---

## Run 20260625-092003-dineout-srs — FAILED

- **When**: 2026-06-25 04:20:03
- **SRS**: dineout_srs.xml  ·  **language**: ?  ·  **stack**: fastapi
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --model deepseek/deepseek-chat --prove --certify --max-cert-loops 6 --stack fastapi`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `deepseek/deepseek-chat` |
| dependency | `deepseek/deepseek-chat` |
| planning | `deepseek/deepseek-chat` |
| code | `deepseek/deepseek-chat` |
| test | `deepseek/deepseek-chat` |
| proof | `deepseek/deepseek-chat` |
| cert | `deepseek/deepseek-chat` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=6
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=6 · baseline=False

- tokens: 5,806 (in 4,781 / out 1,025) · calls 4
- estimated cost: $0.0013

- proved feature ids: (none)

---

## Run 20260628-033707-dineout-srs — COMPLETE

- **When**: 2026-06-27 22:37:07
- **SRS**: dineout_srs.xml  ·  **language**: java  ·  **stack**: spring
- **Command**: `python run_pipeline.py data/srs/dineout_srs.xml --output-dir outputs/matrix/java/dineout_srs/openai_gpt-4_1 --language java --stack spring --model gpt-4.1 --prove --certify --samples 1 --max-cert-loops 4 --prove-rounds 4`

### Models used (per stage)

| stage | model |
|---|---|
| spec | `gpt-4.1` |
| dependency | `gpt-4.1` |
| planning | `gpt-4.1` |
| code | `gpt-4.1` |
| test | `gpt-4.1` |
| proof | `gpt-4.1` |
| cert | `gpt-4.1` |

### Pipeline flags

- agents: spec=on, dependency=on, planning=on, proof=on, code=on, test=on, certify=on, recovery=on
- certify=True · samples=1 · k=[1] · prove=True · max_cert_loops=4
- temperature=0.0 · cert_temperature=0.4 · prove_rounds=4 · baseline=False

### Run metrics (summary)

| metric | value |
|---|---|
| PassVer@1 | 0.5385 |
| verification_pass_ratio | 0.5385 |
| test_case_pass_ratio | 0.0 |
| avg_verification_iteration | 2.81 |
| avg_test_iteration | 1 |
| avg_input_token | 2201.8 |
| avg_output_token | 807.0 |
| total_time (s) | 471.45 |

#### Copy-paste row (TSV — paste directly under your spreadsheet header)

```text
verification_pass_ratio	test_case_pass_ratio	avg_input_token	avg_output_token	total_time	avg_verification_iter	avg_test_iter	PassVer@1
0.5385	0.0	2201.8	807.0	471.45	2.81	1	0.5385
```

- tokens: 258,753 (in 189,354 / out 69,399) · calls 86
- estimated cost: $0.9339

### Dafny proof tier

- proved 4/10 features (rate 0.4)

| feature | result | rounds | axioms |
|---|---|---|---|
| 4.1 | PROVED | 2 | 0 |
| 4.10 | PROVED | 1 | 0 |
| 4.2 | unproved | 4 | 0 |
| 4.3 | unproved | 4 | 0 |
| 4.4 | unproved | 4 | 0 |
| 4.5 | unproved | 4 | 0 |
| 4.6 | unproved | 4 | 0 |
| 4.7 | unproved | 4 | 0 |
| 4.8 | PROVED | 2 | 0 |
| 4.9 | PROVED | 2 | 0 |

### Certification (pass@k)

- pass@1: 0.000
- case pass rate: 0.000
- pass@1 FR ids: (none)

### Final per-feature outcome

| feature | outcome |
|---|---|
| 4.1 | PROVED |
| 4.10 | PROVED |
| 4.8 | PROVED |
| 4.9 | PROVED |

- proved feature ids: ['4.1', '4.10', '4.8', '4.9']

