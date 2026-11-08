# Run report

_SRS: Human.xml · language: python · model: deepseek/deepseek-v3.2_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 6.0
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
- files: 2 · lines of code: 91
- files per layer: {'controller': 2}
- tech stack: F3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 1 · rate: 0.500
  - 3.1 (F3_1): PROVED (6r)
  - 3.2 (F3_2): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 1 · failed: 1
