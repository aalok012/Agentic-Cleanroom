# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 6.0
- **avg_test_iteration**: 1
- **avg_input_token**: 2726.0
- **avg_output_token**: 349.2
- **total_time**: 87.83

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 3.29 | 1,929 | 199 | 2 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 3.56 | 4,930 | 377 | 2 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 50.66 | 40,687 | 3,434 | 12 |
| compile | 0.89 | 0 | 0 | 0 |
| adapter | 5.46 | 1,605 | 628 | 1 |
| code | 2.28 | 1,171 | 252 | 1 |
| test | 18.21 | 4,198 | 2,094 | 2 |
| certification | 3.48 | 0 | 0 | 0 |
| **total** | **87.83** | **54,520** | **6,984** | **20** |

## Tokens & cost

- total tokens: 61,504  (input 54,520 / output 6,984)
- LLM calls: 20
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 2 · lines of code: 91
- files per layer: {'controller': 2}
- tech stack: F3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 2 · test cases: 9

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 1 · rate: 0.500
  - 3.1 (F3_1): PROVED (6r)
  - 3.2 (F3_2): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 1 · failed: 1
