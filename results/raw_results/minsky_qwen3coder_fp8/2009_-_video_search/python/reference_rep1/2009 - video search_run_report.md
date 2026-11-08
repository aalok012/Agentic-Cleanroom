# Run report

_SRS: 2009 - video search.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5714
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5714
- **avg_verification_iteration**: 3.57
- **avg_test_iteration**: 1
- **avg_input_token**: 2599.0
- **avg_output_token**: 429.7
- **total_time**: 248.08

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 6.67 | 6,696 | 739 | 7 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 13.33 | 17,253 | 1,491 | 7 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 124.07 | 89,248 | 10,357 | 25 |
| compile | 4.35 | 0 | 0 | 0 |
| adapter | 6.50 | 1,607 | 754 | 1 |
| adapter | 5.17 | 1,507 | 596 | 1 |
| adapter | 7.30 | 1,523 | 848 | 1 |
| adapter | 4.64 | 1,547 | 533 | 1 |
| code | 10.13 | 3,822 | 1,154 | 3 |
| test | 54.91 | 14,546 | 6,304 | 7 |
| certification | 10.99 | 0 | 0 | 0 |
| **total** | **248.08** | **137,749** | **22,776** | **53** |

## Tokens & cost

- total tokens: 160,525  (input 137,749 / output 22,776)
- LLM calls: 53
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 449
- files per layer: {'controller': 5, 'view': 2}
- tech stack: F3__1__REQ__1Domain, F3__1__REQ__2Domain, F3__1__REQ__3Domain, F3__1__REQ__5Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 7 · test cases: 26

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 7 · proved: 4 · rate: 0.571
  - 3.1.REQ-1 (F3_1_REQ_1): PROVED (4r)
  - 3.1.REQ-2 (F3_1_REQ_2): PROVED (1r)
  - 3.1.REQ-3 (F3_1_REQ_3): PROVED (1r)
  - 3.1.REQ-4 (F3_1_REQ_4): unproved (→ test track) (6r)
  - 3.1.REQ-5 (F3_1_REQ_5): PROVED (1r)
  - 3.1.REQ-6 (F3_1_REQ_6): unproved (→ test track) (6r)
  - 3.1.REQ-7 (F3_1_REQ_7): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 4 · failed: 3
