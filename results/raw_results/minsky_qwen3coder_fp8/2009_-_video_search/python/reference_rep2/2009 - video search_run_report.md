# Run report

_SRS: 2009 - video search.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.2857
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.2857
- **avg_verification_iteration**: 4.57
- **avg_test_iteration**: 1
- **avg_input_token**: 2777.4
- **avg_output_token**: 419.4
- **total_time**: 289.12

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 6.70 | 6,696 | 751 | 7 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 13.32 | 17,251 | 1,495 | 7 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 168.54 | 118,960 | 13,513 | 32 |
| compile | 1.57 | 0 | 0 | 0 |
| adapter | 5.08 | 1,561 | 588 | 1 |
| adapter | 4.70 | 1,538 | 540 | 1 |
| code | 18.90 | 6,076 | 2,165 | 5 |
| test | 53.24 | 14,563 | 6,110 | 7 |
| certification | 17.08 | 0 | 0 | 0 |
| **total** | **289.12** | **166,645** | **25,162** | **60** |

## Tokens & cost

- total tokens: 191,807  (input 166,645 / output 25,162)
- LLM calls: 60
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 367
- files per layer: {'controller': 4, 'model': 1, 'view': 2}
- tech stack: F3__1__REQ__3Domain, F3__1__REQ__5Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 7 · test cases: 27

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 7 · proved: 2 · rate: 0.286
  - 3.1.REQ-1 (F3_1_REQ_1): unproved (→ test track) (6r)
  - 3.1.REQ-2 (F3_1_REQ_2): unproved (→ test track) (6r)
  - 3.1.REQ-3 (F3_1_REQ_3): PROVED (1r)
  - 3.1.REQ-4 (F3_1_REQ_4): unproved (→ test track) (6r)
  - 3.1.REQ-5 (F3_1_REQ_5): PROVED (1r)
  - 3.1.REQ-6 (F3_1_REQ_6): unproved (→ test track) (6r)
  - 3.1.REQ-7 (F3_1_REQ_7): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 2 · failed: 5
