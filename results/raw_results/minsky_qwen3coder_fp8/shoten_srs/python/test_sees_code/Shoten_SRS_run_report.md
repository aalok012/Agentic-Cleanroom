# Run report

_SRS: Shoten_SRS.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.1481
- **test_case_pass_ratio**: 0.4466
- **PassVer@1**: 0.2778
- **avg_verification_iteration**: 5.52
- **avg_test_iteration**: 1
- **avg_input_token**: 3745.1
- **avg_output_token**: 1708.4
- **total_time**: 377.09

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| test | 261.82 | 63,667 | 29,042 | 17 |
| certification | 115.27 | 0 | 0 | 0 |
| **total** | **377.09** | **63,667** | **29,042** | **17** |

## Tokens & cost

- total tokens: 92,709  (input 63,667 / output 29,042)
- LLM calls: 17
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 49 · lines of code: 2,338
- files per layer: {'controller': 26, 'model': 7, 'view': 16}
- tech stack: F4__11Domain, F4__13Domain, F4__3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 17 · test cases: 126

## Certification (pass@k)

- samples n=1
- pass@1: 0.152
- case pass rate: 0.447

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 17 · proved: 3 · rate: 0.176
  - 4.1 (F4_1): unproved (→ test track) (6r)
  - 4.10 (F4_10): unproved (→ test track) (6r)
  - 4.11 (F4_11): PROVED (3r)
  - 4.12 (F4_12): unproved (→ test track) (6r)
  - 4.13 (F4_13): PROVED (3r)
  - 4.14 (F4_14): unproved (→ test track) (6r)
  - 4.15 (F4_15): unproved (→ test track) (6r)
  - 4.2 (F4_2): unproved (→ test track) (6r)
  - 4.3 (F4_3): unproved (→ test track) (6r)
  - 4.3.1 (F4_3_1): PROVED (2r)
  - 4.3.2 (F4_3_2): unproved (→ test track) (6r)
  - 4.4 (F4_4): unproved (→ test track) (6r)
  - 4.5 (F4_5): unproved (→ test track) (6r)
  - 4.6 (F4_6): unproved (→ test track) (6r)
  - 4.7 (F4_7): unproved (→ test track) (6r)
  - 4.8 (F4_8): unproved (→ test track) (6r)
  - 4.9 (F4_9): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 3 · failed: 14
