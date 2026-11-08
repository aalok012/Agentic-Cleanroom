# Run report

_SRS: Shoten_SRS.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0556
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.0556
- **avg_verification_iteration**: 1.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1812.0
- **avg_output_token**: 604.7
- **total_time**: 577.98

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 85.55 | 42,638 | 7,583 | 17 |
| compile | 0.73 | 0 | 0 | 0 |
| adapter | 6.44 | 1,789 | 744 | 1 |
| code | 168.23 | 66,743 | 19,160 | 51 |
| test | 215.43 | 44,661 | 24,521 | 17 |
| certification | 101.60 | 0 | 0 | 0 |
| **total** | **577.98** | **155,831** | **52,008** | **86** |

## Tokens & cost

- total tokens: 207,839  (input 155,831 / output 52,008)
- LLM calls: 86
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 52 · lines of code: 2,249
- files per layer: {'controller': 26, 'model': 7, 'view': 19}
- tech stack: F4__2Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 17 · test cases: 112

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 17 · proved: 1 · rate: 0.059
  - 4.1 (F4_1): unproved (→ test track) (1r)
  - 4.10 (F4_10): unproved (→ test track) (1r)
  - 4.11 (F4_11): unproved (→ test track) (1r)
  - 4.12 (F4_12): unproved (→ test track) (1r)
  - 4.13 (F4_13): unproved (→ test track) (1r)
  - 4.14 (F4_14): unproved (→ test track) (1r)
  - 4.15 (F4_15): unproved (→ test track) (1r)
  - 4.2 (F4_2): PROVED (1r)
  - 4.3 (F4_3): unproved (→ test track) (1r)
  - 4.3.1 (F4_3_1): unproved (→ test track) (1r)
  - 4.3.2 (F4_3_2): unproved (→ test track) (1r)
  - 4.4 (F4_4): unproved (→ test track) (1r)
  - 4.5 (F4_5): unproved (→ test track) (1r)
  - 4.6 (F4_6): unproved (→ test track) (1r)
  - 4.7 (F4_7): unproved (→ test track) (1r)
  - 4.8 (F4_8): unproved (→ test track) (1r)
  - 4.9 (F4_9): unproved (→ test track) (1r)

## Native compile (dafny translate py)

- compiled: 1 · failed: 16
