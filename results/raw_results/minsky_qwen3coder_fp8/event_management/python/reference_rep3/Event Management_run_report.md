# Run report

_SRS: Event Management.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 3.5
- **avg_test_iteration**: 1
- **avg_input_token**: 2453.4
- **avg_output_token**: 385.2
- **total_time**: 406.99

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.01 | 0 | 0 | 0 |
| spec_contracts | 10.05 | 11,400 | 1,114 | 12 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 21.20 | 29,368 | 2,383 | 12 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 185.56 | 138,322 | 12,679 | 42 |
| compile | 6.59 | 0 | 0 | 0 |
| adapter | 4.67 | 1,484 | 536 | 1 |
| adapter | 5.60 | 1,538 | 657 | 1 |
| adapter | 5.15 | 1,547 | 594 | 1 |
| adapter | 4.75 | 1,474 | 546 | 1 |
| adapter | 4.95 | 1,602 | 570 | 1 |
| adapter | 5.03 | 1,533 | 589 | 1 |
| code | 29.03 | 7,791 | 3,355 | 6 |
| test | 100.72 | 24,748 | 11,649 | 12 |
| certification | 23.69 | 0 | 0 | 0 |
| **total** | **406.99** | **220,807** | **34,672** | **90** |

## Tokens & cost

- total tokens: 255,479  (input 220,807 / output 34,672)
- LLM calls: 90
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 12 · lines of code: 736
- files per layer: {'controller': 10, 'model': 2}
- tech stack: F3__2__REQ__10Domain, F3__2__REQ__11Domain, F3__2__REQ__12Domain, F3__2__REQ__1Domain, F3__2__REQ__3Domain, F3__2__REQ__5Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 12 · test cases: 48

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 12 · proved: 6 · rate: 0.500
  - 3.2.REQ-1 (F3_2_REQ_1): PROVED (1r)
  - 3.2.REQ-10 (F3_2_REQ_10): PROVED (1r)
  - 3.2.REQ-11 (F3_2_REQ_11): PROVED (1r)
  - 3.2.REQ-12 (F3_2_REQ_12): PROVED (1r)
  - 3.2.REQ-2 (F3_2_REQ_2): unproved (→ test track) (6r)
  - 3.2.REQ-3 (F3_2_REQ_3): PROVED (1r)
  - 3.2.REQ-4 (F3_2_REQ_4): unproved (→ test track) (6r)
  - 3.2.REQ-5 (F3_2_REQ_5): PROVED (1r)
  - 3.2.REQ-6 (F3_2_REQ_6): unproved (→ test track) (6r)
  - 3.2.REQ-7 (F3_2_REQ_7): unproved (→ test track) (6r)
  - 3.2.REQ-8 (F3_2_REQ_8): unproved (→ test track) (6r)
  - 3.2.REQ-9 (F3_2_REQ_9): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 6 · failed: 6
