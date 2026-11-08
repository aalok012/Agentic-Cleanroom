# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0
- **test_case_pass_ratio**: 0.2222
- **PassVer@1**: 0.0
- **avg_verification_iteration**: 0.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1660.5
- **avg_output_token**: 790.5
- **total_time**: 34.66

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| code | 6.47 | 2,444 | 737 | 2 |
| test | 20.87 | 4,198 | 2,425 | 2 |
| certification | 7.32 | 0 | 0 | 0 |
| **total** | **34.66** | **6,642** | **3,162** | **4** |

## Tokens & cost

- total tokens: 9,804  (input 6,642 / output 3,162)
- LLM calls: 4
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 2 · lines of code: 85
- files per layer: {'controller': 2}
- tech stack: app, fastapi, sqlalchemy

## Generated tests

- features: 2 · test cases: 9

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.222
