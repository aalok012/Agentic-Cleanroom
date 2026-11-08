# Run report

_SRS: Shoten_SRS.xml · language: python · model: deepseek/deepseek-v3.2_

## Run metrics

- **verification_pass_ratio**: 0.1481
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.1481
- **avg_verification_iteration**: 5.52
- **avg_test_iteration**: 0.0
- **avg_input_token**: 0.0
- **avg_output_token**: 0.0
- **total_time**: 0

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| **total** | **0.00** | **0** | **0** | **0** |

## Tokens & cost

- total tokens: 0  (input 0 / output 0)
- LLM calls: 0
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 49 · lines of code: 2,338
- files per layer: {'controller': 26, 'model': 7, 'view': 16}
- tech stack: F4__11Domain, F4__13Domain, F4__3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

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
