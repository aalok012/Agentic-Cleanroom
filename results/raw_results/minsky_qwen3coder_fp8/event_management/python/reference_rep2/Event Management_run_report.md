# Run report

_SRS: Event Management.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.6667
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.6667
- **avg_verification_iteration**: 2.92
- **avg_test_iteration**: 1
- **avg_input_token**: 2339.8
- **avg_output_token**: 396.3
- **total_time**: 365.88

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.01 | 0 | 0 | 0 |
| spec_contracts | 10.03 | 11,400 | 1,114 | 12 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 21.13 | 29,368 | 2,373 | 12 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 149.30 | 111,266 | 10,739 | 35 |
| compile | 8.78 | 0 | 0 | 0 |
| adapter | 5.54 | 1,484 | 642 | 1 |
| adapter | 4.93 | 1,538 | 568 | 1 |
| adapter | 4.47 | 1,527 | 514 | 1 |
| adapter | 5.76 | 1,474 | 666 | 1 |
| adapter | 5.54 | 1,552 | 640 | 1 |
| adapter | 5.23 | 1,533 | 602 | 1 |
| adapter | 6.20 | 1,591 | 716 | 1 |
| adapter | 6.62 | 1,631 | 765 | 1 |
| code | 16.87 | 5,114 | 1,937 | 4 |
| test | 101.03 | 24,726 | 11,614 | 12 |
| certification | 14.44 | 0 | 0 | 0 |
| **total** | **365.88** | **194,204** | **32,890** | **83** |

## Tokens & cost

- total tokens: 227,094  (input 194,204 / output 32,890)
- LLM calls: 83
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 12 · lines of code: 775
- files per layer: {'controller': 10, 'model': 2}
- tech stack: F3__2__REQ__10Domain, F3__2__REQ__11Domain, F3__2__REQ__12Domain, F3__2__REQ__1Domain, F3__2__REQ__3Domain, F3__2__REQ__5Domain, F3__2__REQ__8Domain, F3__2__REQ__9Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 12 · test cases: 48

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 12 · proved: 8 · rate: 0.667
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
  - 3.2.REQ-8 (F3_2_REQ_8): PROVED (1r)
  - 3.2.REQ-9 (F3_2_REQ_9): PROVED (4r)

## Native compile (dafny translate py)

- compiled: 8 · failed: 4
