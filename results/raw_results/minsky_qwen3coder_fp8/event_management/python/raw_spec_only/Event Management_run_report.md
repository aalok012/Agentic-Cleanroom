# Run report

_SRS: Event Management.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 3.92
- **avg_test_iteration**: 1
- **avg_input_token**: 2718.1
- **avg_output_token**: 388.6
- **total_time**: 332.69

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.01 | 0 | 0 | 0 |
| spec_contracts | 0.00 | 0 | 0 | 0 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 0.00 | 0 | 0 | 0 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 183.75 | 153,730 | 13,326 | 47 |
| compile | 6.45 | 0 | 0 | 0 |
| adapter | 5.77 | 1,506 | 667 | 1 |
| adapter | 5.70 | 1,517 | 658 | 1 |
| adapter | 4.96 | 1,487 | 572 | 1 |
| adapter | 6.33 | 1,705 | 729 | 1 |
| adapter | 5.18 | 1,505 | 594 | 1 |
| adapter | 5.69 | 1,508 | 656 | 1 |
| code | 15.93 | 6,388 | 1,800 | 6 |
| test | 74.91 | 23,640 | 8,586 | 12 |
| certification | 18.02 | 0 | 0 | 0 |
| **total** | **332.69** | **192,986** | **27,588** | **71** |

## Tokens & cost

- total tokens: 220,574  (input 192,986 / output 27,588)
- LLM calls: 71
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 12 · lines of code: 637
- files per layer: {'controller': 12}
- tech stack: F3__2__REQ__10Domain, F3__2__REQ__4Domain, F3__2__REQ__5Domain, F3__2__REQ__7Domain, F3__2__REQ__8Domain, F3__2__REQ__9Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 12 · test cases: 47

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 12 · proved: 6 · rate: 0.500
  - 3.2.REQ-1 (F3_2_REQ_1): unproved (→ test track) (6r)
  - 3.2.REQ-10 (F3_2_REQ_10): PROVED (1r)
  - 3.2.REQ-11 (F3_2_REQ_11): unproved (→ test track) (6r)
  - 3.2.REQ-12 (F3_2_REQ_12): unproved (→ test track) (6r)
  - 3.2.REQ-2 (F3_2_REQ_2): unproved (→ test track) (6r)
  - 3.2.REQ-3 (F3_2_REQ_3): unproved (→ test track) (6r)
  - 3.2.REQ-4 (F3_2_REQ_4): PROVED (1r)
  - 3.2.REQ-5 (F3_2_REQ_5): PROVED (1r)
  - 3.2.REQ-6 (F3_2_REQ_6): unproved (→ test track) (6r)
  - 3.2.REQ-7 (F3_2_REQ_7): PROVED (1r)
  - 3.2.REQ-8 (F3_2_REQ_8): PROVED (6r)
  - 3.2.REQ-9 (F3_2_REQ_9): PROVED (1r)

## Native compile (dafny translate py)

- compiled: 6 · failed: 6
