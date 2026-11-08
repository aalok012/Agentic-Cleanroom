# Run report

_SRS: Shoten_SRS.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.1481
- **test_case_pass_ratio**: 0.4211
- **PassVer@1**: 0.2222
- **avg_verification_iteration**: 5.52
- **avg_test_iteration**: 1
- **avg_input_token**: 2677.0
- **avg_output_token**: 519.6
- **total_time**: 1173.25

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 47.83 | 17,281 | 5,579 | 17 |
| dependency | 9.18 | 12,685 | 970 | 15 |
| planning | 104.86 | 45,644 | 11,957 | 17 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 500.58 | 367,042 | 43,644 | 92 |
| compile | 3.00 | 0 | 0 | 0 |
| adapter | 8.69 | 2,154 | 997 | 1 |
| adapter | 6.66 | 1,839 | 767 | 1 |
| adapter | 6.98 | 1,760 | 805 | 1 |
| code | 158.06 | 60,720 | 18,008 | 46 |
| test | 218.57 | 45,013 | 24,835 | 17 |
| certification | 108.84 | 0 | 0 | 0 |
| **total** | **1173.25** | **554,138** | **107,562** | **207** |

## Tokens & cost

- total tokens: 661,700  (input 554,138 / output 107,562)
- LLM calls: 207
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 49 · lines of code: 2,332
- files per layer: {'controller': 26, 'model': 7, 'view': 16}
- tech stack: F4__11Domain, F4__13Domain, F4__3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 17 · test cases: 115

## Certification (pass@k)

- samples n=1
- pass@1: 0.087
- case pass rate: 0.421

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
