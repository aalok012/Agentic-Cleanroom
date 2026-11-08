# Run report

_SRS: Event Management.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.6667
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.6667
- **avg_verification_iteration**: 1.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1939.5
- **avg_output_token**: 579.3
- **total_time**: 221.85

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 46.13 | 28,059 | 3,055 | 12 |
| compile | 8.94 | 0 | 0 | 0 |
| adapter | 5.57 | 1,542 | 644 | 1 |
| adapter | 5.23 | 1,548 | 606 | 1 |
| adapter | 5.28 | 1,478 | 609 | 1 |
| adapter | 5.41 | 1,523 | 624 | 1 |
| adapter | 4.62 | 1,592 | 529 | 1 |
| adapter | 7.37 | 1,585 | 854 | 1 |
| adapter | 6.14 | 1,638 | 708 | 1 |
| adapter | 5.83 | 1,573 | 672 | 1 |
| code | 12.14 | 4,793 | 1,417 | 4 |
| test | 95.89 | 24,490 | 11,137 | 12 |
| certification | 13.31 | 0 | 0 | 0 |
| **total** | **221.85** | **69,821** | **20,855** | **36** |

## Tokens & cost

- total tokens: 90,676  (input 69,821 / output 20,855)
- LLM calls: 36
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 12 · lines of code: 742
- files per layer: {'controller': 10, 'model': 1, 'view': 1}
- tech stack: F3__2__REQ__10Domain, F3__2__REQ__11Domain, F3__2__REQ__12Domain, F3__2__REQ__5Domain, F3__2__REQ__6Domain, F3__2__REQ__7Domain, F3__2__REQ__8Domain, F3__2__REQ__9Domain, app, dafny_marshal, fastapi, pydantic, sqlalchemy

## Generated tests

- features: 12 · test cases: 49

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 12 · proved: 8 · rate: 0.667
  - 3.2.REQ-1 (F3_2_REQ_1): unproved (→ test track) (1r)
  - 3.2.REQ-10 (F3_2_REQ_10): PROVED (1r)
  - 3.2.REQ-11 (F3_2_REQ_11): PROVED (1r)
  - 3.2.REQ-12 (F3_2_REQ_12): PROVED (1r)
  - 3.2.REQ-2 (F3_2_REQ_2): unproved (→ test track) (1r)
  - 3.2.REQ-3 (F3_2_REQ_3): unproved (→ test track) (1r)
  - 3.2.REQ-4 (F3_2_REQ_4): unproved (→ test track) (1r)
  - 3.2.REQ-5 (F3_2_REQ_5): PROVED (1r)
  - 3.2.REQ-6 (F3_2_REQ_6): PROVED (1r)
  - 3.2.REQ-7 (F3_2_REQ_7): PROVED (1r)
  - 3.2.REQ-8 (F3_2_REQ_8): PROVED (1r)
  - 3.2.REQ-9 (F3_2_REQ_9): PROVED (1r)

## Native compile (dafny translate py)

- compiled: 8 · failed: 4
