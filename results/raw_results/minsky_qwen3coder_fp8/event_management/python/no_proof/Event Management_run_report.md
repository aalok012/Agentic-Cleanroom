# Run report

_SRS: Event Management.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.0
- **test_case_pass_ratio**: 0.36
- **PassVer@1**: 0.0833
- **avg_verification_iteration**: 0.0
- **avg_test_iteration**: 1
- **avg_input_token**: 1607.3
- **avg_output_token**: 637.5
- **total_time**: 178.97

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| code | 33.94 | 14,085 | 3,846 | 12 |
| test | 98.85 | 24,490 | 11,455 | 12 |
| certification | 46.19 | 0 | 0 | 0 |
| **total** | **178.97** | **38,575** | **15,301** | **24** |

## Tokens & cost

- total tokens: 53,876  (input 38,575 / output 15,301)
- LLM calls: 24
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 12 · lines of code: 462
- files per layer: {'model': 4, 'controller': 6, 'view': 2}
- tech stack: app, fastapi, sqlalchemy

## Generated tests

- features: 12 · test cases: 50

## Certification (pass@k)

- samples n=1
- pass@1: 0.083
- case pass rate: 0.360
