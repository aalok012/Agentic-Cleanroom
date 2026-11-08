# Run report

_SRS: 2009 - video search.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5714
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5714
- **avg_verification_iteration**: 3.14
- **avg_test_iteration**: 1
- **avg_input_token**: 2581.4
- **avg_output_token**: 413.8
- **total_time**: 237.06

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 6.72 | 6,696 | 751 | 7 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 13.89 | 17,251 | 1,566 | 7 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 118.59 | 80,512 | 8,561 | 22 |
| compile | 3.98 | 0 | 0 | 0 |
| adapter | 6.10 | 1,604 | 706 | 1 |
| adapter | 5.17 | 1,545 | 595 | 1 |
| adapter | 4.94 | 1,538 | 578 | 1 |
| adapter | 6.10 | 1,686 | 703 | 1 |
| code | 9.53 | 3,630 | 1,083 | 3 |
| test | 53.47 | 14,609 | 6,149 | 7 |
| certification | 8.58 | 0 | 0 | 0 |
| **total** | **237.06** | **129,071** | **20,692** | **50** |

## Tokens & cost

- total tokens: 149,763  (input 129,071 / output 20,692)
- LLM calls: 50
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 421
- files per layer: {'controller': 5, 'model': 1, 'view': 1}
- tech stack: F3__1__REQ__1Domain, F3__1__REQ__3Domain, F3__1__REQ__5Domain, F3__1__REQ__6Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 7 · test cases: 26

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 7 · proved: 4 · rate: 0.571
  - 3.1.REQ-1 (F3_1_REQ_1): PROVED (1r)
  - 3.1.REQ-2 (F3_1_REQ_2): unproved (→ test track) (6r)
  - 3.1.REQ-3 (F3_1_REQ_3): PROVED (1r)
  - 3.1.REQ-4 (F3_1_REQ_4): unproved (→ test track) (6r)
  - 3.1.REQ-5 (F3_1_REQ_5): PROVED (1r)
  - 3.1.REQ-6 (F3_1_REQ_6): PROVED (1r)
  - 3.1.REQ-7 (F3_1_REQ_7): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 4 · failed: 3
