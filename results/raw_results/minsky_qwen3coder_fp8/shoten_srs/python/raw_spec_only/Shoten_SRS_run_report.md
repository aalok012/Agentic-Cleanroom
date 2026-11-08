# Run report

_SRS: Shoten_SRS.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.2407
- **test_case_pass_ratio**: 0.3929
- **PassVer@1**: 0.2407
- **avg_verification_iteration**: 5.13
- **avg_test_iteration**: 1
- **avg_input_token**: 2569.0
- **avg_output_token**: 465.2
- **total_time**: 898.92

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 0.00 | 0 | 0 | 0 |
| dependency | 9.21 | 12,685 | 970 | 15 |
| planning | 0.00 | 0 | 0 | 0 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 441.77 | 315,073 | 34,804 | 86 |
| compile | 4.53 | 0 | 0 | 0 |
| adapter | 11.13 | 2,209 | 1,281 | 1 |
| adapter | 6.03 | 1,521 | 696 | 1 |
| adapter | 8.42 | 1,761 | 973 | 1 |
| adapter | 10.52 | 2,266 | 1,208 | 1 |
| code | 119.72 | 43,967 | 13,626 | 41 |
| test | 194.38 | 39,264 | 22,271 | 17 |
| certification | 93.22 | 0 | 0 | 0 |
| **total** | **898.92** | **418,746** | **75,829** | **163** |

## Tokens & cost

- total tokens: 494,575  (input 418,746 / output 75,829)
- LLM calls: 163
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 45 · lines of code: 2,042
- files per layer: {'controller': 45}
- tech stack: F4__10Domain, F4__14Domain, F4__5Domain, F4__6Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 17 · test cases: 112

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.393

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 17 · proved: 4 · rate: 0.235
  - 4.1 (F4_1): unproved (→ test track) (6r)
  - 4.10 (F4_10): PROVED (2r)
  - 4.11 (F4_11): unproved (→ test track) (6r)
  - 4.12 (F4_12): unproved (→ test track) (6r)
  - 4.13 (F4_13): unproved (→ test track) (6r)
  - 4.14 (F4_14): PROVED (1r)
  - 4.15 (F4_15): unproved (→ test track) (6r)
  - 4.2 (F4_2): unproved (→ test track) (6r)
  - 4.3 (F4_3): unproved (→ test track) (6r)
  - 4.3.1 (F4_3_1): unproved (→ test track) (6r)
  - 4.3.2 (F4_3_2): unproved (→ test track) (6r)
  - 4.4 (F4_4): unproved (→ test track) (6r)
  - 4.5 (F4_5): PROVED (2r)
  - 4.6 (F4_6): PROVED (3r)
  - 4.7 (F4_7): unproved (→ test track) (6r)
  - 4.8 (F4_8): unproved (→ test track) (6r)
  - 4.9 (F4_9): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 4 · failed: 13
