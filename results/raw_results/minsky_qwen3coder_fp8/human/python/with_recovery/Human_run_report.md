# Run report

_SRS: Human.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 1.0
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 1.0
- **avg_verification_iteration**: 6.0
- **avg_test_iteration**: 0.0
- **avg_input_token**: 1953.5
- **avg_output_token**: 465.5
- **total_time**: 14.78

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| certification | 3.46 | 0 | 0 | 0 |
| recovery | 11.32 | 3,907 | 931 | 2 |
| **total** | **14.78** | **3,907** | **931** | **2** |

## Tokens & cost

- total tokens: 4,838  (input 3,907 / output 931)
- LLM calls: 2
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 2 · lines of code: 91
- files per layer: {'controller': 2}
- tech stack: F3__1Domain, app, dafny_marshal, fastapi, sqlalchemy

## Generated tests

- features: 2 · test cases: 9

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Recovery loop (re-prove + test-informed regen)

- passes run: 1 / 2 max
- re-proved (now ship from Dafny): ['3.2']
- repaired with test feedback (clean-room relaxed): (none)
- still UNCERTIFIED: (none)

Final per-feature certification label:
  - 3.1: PROVED
  - 3.2: PROVED (recovery)

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 2 · proved: 1 · rate: 0.500
  - 3.1 (F3_1): PROVED (6r)
  - 3.2 (F3_2): unproved (→ test track) (6r)

## Native compile (dafny translate py)

- compiled: 1 · failed: 1
