# Run report

_SRS: Shoten_SRS.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.0
- **avg_verification_iteration**: 0.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1622.0
- **avg_output_token**: 628.9
- **total_time**: 499.2

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| code | 176.47 | 70,498 | 20,114 | 54 |
| test | 214.58 | 44,661 | 24,541 | 17 |
| certification | 108.16 | 0 | 0 | 0 |
| **total** | **499.20** | **115,159** | **44,655** | **71** |

## Tokens & cost

- total tokens: 159,814  (input 115,159 / output 44,655)
- LLM calls: 71
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 54 · lines of code: 2,284
- files per layer: {'controller': 27, 'model': 8, 'view': 19}
- tech stack: app, fastapi, sqlalchemy

## Generated tests

- features: 17 · test cases: 113

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000
