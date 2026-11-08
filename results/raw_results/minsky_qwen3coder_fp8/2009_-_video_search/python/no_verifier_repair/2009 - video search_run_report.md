# Run report

_SRS: 2009 - video search.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.4286
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.4286
- **avg_verification_iteration**: 1.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1933.6
- **avg_output_token**: 587.6
- **total_time**: 133.87

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 32.65 | 16,470 | 2,495 | 7 |
| compile | 2.81 | 0 | 0 | 0 |
| adapter | 5.19 | 1,608 | 597 | 1 |
| adapter | 4.84 | 1,523 | 557 | 1 |
| adapter | 6.04 | 1,547 | 699 | 1 |
| code | 12.83 | 4,912 | 1,500 | 4 |
| test | 55.92 | 14,546 | 6,491 | 7 |
| certification | 13.59 | 0 | 0 | 0 |
| **total** | **133.87** | **40,606** | **12,339** | **21** |

## Tokens & cost

- total tokens: 52,945  (input 40,606 / output 12,339)
- LLM calls: 21
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 370
- files per layer: {'controller': 4, 'model': 1, 'view': 2}
- tech stack: F3__1__REQ__1Domain, F3__1__REQ__3Domain, F3__1__REQ__5Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 7 · test cases: 28

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 7 · proved: 3 · rate: 0.429
  - 3.1.REQ-1 (F3_1_REQ_1): PROVED (1r)
  - 3.1.REQ-2 (F3_1_REQ_2): unproved (→ test track) (1r)
  - 3.1.REQ-3 (F3_1_REQ_3): PROVED (1r)
  - 3.1.REQ-4 (F3_1_REQ_4): unproved (→ test track) (1r)
  - 3.1.REQ-5 (F3_1_REQ_5): PROVED (1r)
  - 3.1.REQ-6 (F3_1_REQ_6): unproved (→ test track) (1r)
  - 3.1.REQ-7 (F3_1_REQ_7): unproved (→ test track) (1r)

## Native compile (dafny translate py)

- compiled: 3 · failed: 4
