# Run report

_SRS: Human.xml · language: java · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.5
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.5
- **avg_verification_iteration**: 6.0
- **avg_test_iteration**: 1
- **avg_input_token**: 3036.5
- **avg_output_token**: 406.2
- **total_time**: 126.14

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| spec_parse | 0.00 | 0 | 0 | 0 |
| spec_contracts | 3.34 | 1,929 | 199 | 2 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 3.48 | 4,856 | 369 | 2 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 51.54 | 40,687 | 3,434 | 12 |
| compile | 1.19 | 0 | 0 | 0 |
| adapter | 8.42 | 3,111 | 939 | 1 |
| code | 1.81 | 1,240 | 200 | 1 |
| test | 18.41 | 3,315 | 2,126 | 2 |
| java_compile_repair | 33.57 | 14,702 | 2,076 | 3 |
| certification | 4.38 | 0 | 0 | 0 |
| **total** | **126.14** | **69,840** | **9,343** | **23** |

## Tokens & cost

- total tokens: 79,183  (input 69,840 / output 9,343)
- LLM calls: 23
- estimated cost: $0.0000

## Generated code

- language: Java
- files: 2 · lines of code: 83
- files per layer: {'controller': 2}
- tech stack: Python standard library only

## Generated tests

- features: 2 · test cases: 8

## Java compile repair

- status: failed
- checks: 3 · repaired files: 3
- reason: mvn clean test-compile failed

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 1 · rate: 0.500
  - 3.1 (F3_1): PROVED (6r)
  - 3.2 (F3_2): unproved (→ test track) (6r)

## Native compile (dafny translate java)

- compiled: 1 · failed: 1
