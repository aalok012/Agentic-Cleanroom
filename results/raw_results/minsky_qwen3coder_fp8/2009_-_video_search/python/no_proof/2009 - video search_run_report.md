# Run report

_SRS: 2009 - video search.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0
- **test_case_pass_ratio**: 0.4074
- **PassVer@1**: 0.1429
- **avg_verification_iteration**: 0.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1635.6
- **avg_output_token**: 614.4
- **total_time**: 98.5

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| code | 22.85 | 8,353 | 2,603 | 7 |
| test | 51.75 | 14,546 | 5,999 | 7 |
| certification | 23.91 | 0 | 0 | 0 |
| **total** | **98.50** | **22,899** | **8,602** | **14** |

## Tokens & cost

- total tokens: 31,501  (input 22,899 / output 8,602)
- LLM calls: 14
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 7 · lines of code: 290
- files per layer: {'controller': 3, 'model': 1, 'view': 3}
- tech stack: app, fastapi, sqlalchemy

## Generated tests

- features: 7 · test cases: 27

## Certification (pass@k)

- samples n=1
- pass@1: 0.143
- case pass rate: 0.407
