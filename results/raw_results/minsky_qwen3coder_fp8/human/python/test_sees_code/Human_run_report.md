# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 6.0
- **avg_test_iteration**: 1
- **avg_input_token**: 2509.0
- **avg_output_token**: 1256.0
- **total_time**: 25.39

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| test | 21.92 | 5,018 | 2,512 | 2 |
| certification | 3.47 | 0 | 0 | 0 |
| **total** | **25.39** | **5,018** | **2,512** | **2** |

## Tokens & cost

- total tokens: 7,530  (input 5,018 / output 2,512)
- LLM calls: 2
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
