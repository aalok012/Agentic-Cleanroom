# Run report

_SRS: Shoten_SRS.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.1481
- **test_case_pass_ratio**: 0.4444
- **PassVer@1**: 0.2778
- **avg_verification_iteration**: 5.52
- **avg_test_iteration**: 1
- **avg_input_token**: 2674.5
- **avg_output_token**: 513.2
- **total_time**: 1154.61

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 47.88 | 17,281 | 5,578 | 17 |
| dependency | 9.22 | 12,685 | 970 | 15 |
| planning | 98.62 | 45,643 | 11,251 | 17 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 497.84 | 367,466 | 43,322 | 92 |
| compile | 2.71 | 0 | 0 | 0 |
| adapter | 6.70 | 2,154 | 770 | 1 |
| adapter | 15.62 | 1,841 | 1,809 | 1 |
| adapter | 7.49 | 1,752 | 866 | 1 |
| code | 154.91 | 60,147 | 17,655 | 46 |
| test | 210.87 | 44,661 | 24,011 | 17 |
| certification | 102.74 | 0 | 0 | 0 |
| **total** | **1154.61** | **553,630** | **106,232** | **207** |

## Tokens & cost

- total tokens: 659,862  (input 553,630 / output 106,232)
- LLM calls: 207
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 49 · lines of code: 2,338
- files per layer: {'controller': 26, 'model': 7, 'view': 16}
- tech stack: F4__11Domain, F4__13Domain, F4__3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 17 · test cases: 111

## Certification (pass@k)

- samples n=1
- pass@1: 0.152
- case pass rate: 0.444

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
