# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.6
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 3.5
- **avg_test_iteration**: 1
- **avg_input_token**: 2572.3
- **avg_output_token**: 391.4
- **total_time**: 69.7

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 1.93 | 1,929 | 211 | 2 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 3.63 | 4,942 | 408 | 2 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 33.45 | 24,571 | 2,356 | 7 |
| compile | 1.11 | 0 | 0 | 0 |
| adapter | 6.54 | 1,565 | 759 | 1 |
| code | 3.80 | 1,338 | 433 | 1 |
| test | 14.87 | 4,239 | 1,704 | 2 |
| certification | 4.37 | 0 | 0 | 0 |
| **total** | **69.70** | **38,584** | **5,871** | **15** |

## Tokens & cost

- total tokens: 44,455  (input 38,584 / output 5,871)
- LLM calls: 15
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 2 · lines of code: 133
- files per layer: {'controller': 2}
- tech stack: F3__2Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 2 · test cases: 7

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.600

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 1 · rate: 0.500
  - 3.1 (F3_1): unproved (→ test track) (6r)
  - 3.2 (F3_2): PROVED (1r)

## Native compile (dafny translate py)

- compiled: 1 · failed: 1
