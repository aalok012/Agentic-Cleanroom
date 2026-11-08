# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0
- **test_case_pass_ratio**: 0.4
- **PassVer@1**: 0.0
- **avg_verification_iteration**: 6.0
- **avg_test_iteration**: 1
- **avg_input_token**: 3004.8
- **avg_output_token**: 440.6
- **total_time**: 84.51

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 0.00 | 0 | 0 | 0 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 0.00 | 0 | 0 | 0 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 51.49 | 41,774 | 4,184 | 12 |
| compile | 0.00 | 0 | 0 | 0 |
| code | 5.84 | 2,210 | 668 | 2 |
| test | 19.07 | 4,092 | 2,198 | 2 |
| certification | 8.11 | 0 | 0 | 0 |
| **total** | **84.51** | **48,076** | **7,050** | **16** |

## Tokens & cost

- total tokens: 55,126  (input 48,076 / output 7,050)
- LLM calls: 16
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 2 · lines of code: 87
- files per layer: {'controller': 2}
- tech stack: app, fastapi, sqlalchemy

## Generated tests

- features: 2 · test cases: 10

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.400

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 0 · rate: 0.000
  - 3.1 (F3_1): unproved (→ test track) (6r)
  - 3.2 (F3_2): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 0 · failed: 2
