# Run report

_SRS: 2009 - video search.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5714
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5714
- **avg_verification_iteration**: 3.14
- **avg_test_iteration**: 1
- **avg_input_token**: 2625.7
- **avg_output_token**: 411.0
- **total_time**: 187.41

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 0.00 | 0 | 0 | 0 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 0.00 | 0 | 0 | 0 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 101.01 | 71,397 | 6,569 | 22 |
| compile | 4.53 | 0 | 0 | 0 |
| adapter | 5.80 | 1,492 | 671 | 1 |
| adapter | 4.80 | 1,476 | 552 | 1 |
| adapter | 4.94 | 1,490 | 570 | 1 |
| adapter | 5.19 | 1,552 | 599 | 1 |
| code | 9.91 | 3,222 | 1,134 | 3 |
| test | 41.03 | 13,896 | 4,701 | 7 |
| certification | 10.21 | 0 | 0 | 0 |
| **total** | **187.41** | **94,525** | **14,796** | **36** |

## Tokens & cost

- total tokens: 109,321  (input 94,525 / output 14,796)
- LLM calls: 36
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 408
- files per layer: {'controller': 7}
- tech stack: F3__1__REQ__1Domain, F3__1__REQ__2Domain, F3__1__REQ__3Domain, F3__1__REQ__5Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 7 · test cases: 27

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 7 · proved: 4 · rate: 0.571
  - 3.1.REQ-1 (F3_1_REQ_1): PROVED (1r)
  - 3.1.REQ-2 (F3_1_REQ_2): PROVED (1r)
  - 3.1.REQ-3 (F3_1_REQ_3): PROVED (1r)
  - 3.1.REQ-4 (F3_1_REQ_4): unproved (→ test track) (6r)
  - 3.1.REQ-5 (F3_1_REQ_5): PROVED (1r)
  - 3.1.REQ-6 (F3_1_REQ_6): unproved (→ test track) (6r)
  - 3.1.REQ-7 (F3_1_REQ_7): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 4 · failed: 3
