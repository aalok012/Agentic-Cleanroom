# Run report

_SRS: 2009 - video search.xml · language: python · model: deepseek/deepseek-v3.2_

## Run metrics

- **verification_pass_ratio**: 0.5714
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5714
- **avg_verification_iteration**: 3.57
- **avg_test_iteration**: 0.0
- **avg_input_token**: 0.0
- **avg_output_token**: 0.0
- **total_time**: 0

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| **total** | **0.00** | **0** | **0** | **0** |

## Tokens & cost

- total tokens: 0  (input 0 / output 0)
- LLM calls: 0
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 449
- files per layer: {'controller': 5, 'view': 2}
- tech stack: F3__1__REQ__1Domain, F3__1__REQ__2Domain, F3__1__REQ__3Domain, F3__1__REQ__5Domain, app, dafny_marshal, fastapi, sqlalchemy

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
