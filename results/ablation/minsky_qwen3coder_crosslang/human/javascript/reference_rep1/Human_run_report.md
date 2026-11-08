# Run report

_SRS: Human.xml · language: javascript · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.75
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 3.5
- **avg_test_iteration**: 1
- **avg_input_token**: 2472.1
- **avg_output_token**: 339.1
- **total_time**: 58.91

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 1.92 | 1,929 | 211 | 2 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 3.58 | 4,868 | 399 | 2 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 33.56 | 24,571 | 2,356 | 7 |
| compile | 1.11 | 0 | 0 | 0 |
| code | 3.52 | 2,193 | 390 | 2 |
| test | 15.04 | 3,520 | 1,730 | 2 |
| certification | 0.17 | 0 | 0 | 0 |
| **total** | **58.91** | **37,081** | **5,086** | **15** |

## Tokens & cost

- total tokens: 42,167  (input 37,081 / output 5,086)
- LLM calls: 15
- estimated cost: $0.0000

## Generated code

- language: JavaScript
- files: 2 · lines of code: 42
- files per layer: {'controller': 2}
- tech stack: Python standard library only

## Generated tests

- features: 2 · test cases: 8

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.750

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 1 · rate: 0.500
  - 3.1 (F3_1): unproved (→ test track) (6r)
  - 3.2 (F3_2): PROVED (1r)

## Native compile (dafny translate py)

- compiled: 1 · failed: 1
