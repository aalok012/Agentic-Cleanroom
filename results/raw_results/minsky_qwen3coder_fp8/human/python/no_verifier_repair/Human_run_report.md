# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0
- **test_case_pass_ratio**: 0.125
- **PassVer@1**: 0.0
- **avg_verification_iteration**: 1.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1880.5
- **avg_output_token**: 503.5
- **total_time**: 34.4

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 6.39 | 4,641 | 566 | 2 |
| compile | 0.00 | 0 | 0 | 0 |
| code | 6.07 | 2,444 | 707 | 2 |
| test | 15.04 | 4,198 | 1,748 | 2 |
| certification | 6.91 | 0 | 0 | 0 |
| **total** | **34.40** | **11,283** | **3,021** | **6** |

## Tokens & cost

- total tokens: 14,304  (input 11,283 / output 3,021)
- LLM calls: 6
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 2 · lines of code: 83
- files per layer: {'controller': 2}
- tech stack: app, fastapi, sqlalchemy

## Generated tests

- features: 2 · test cases: 8

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.125

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 0 · rate: 0.000
  - 3.1 (F3_1): unproved (→ test track) (1r)
  - 3.2 (F3_2): unproved (→ test track) (1r)

## Native compile (dafny translate py)

- compiled: 0 · failed: 2
