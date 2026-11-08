# Run report

_SRS: Event Management.xml · language: python · model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8_

## Run metrics

- **verification_pass_ratio**: 0.8333
- **test_case_pass_ratio**: 0.0
- **PassVer@1**: 0.8333
- **avg_verification_iteration**: 2.75
- **avg_test_iteration**: 3
- **avg_input_token**: 3367.6
- **avg_output_token**: 344.5
- **total_time**: 201.5

## Timing & tokens (per stage)

| stage | seconds | input tok | output tok | calls |
|---|---|---|---|---|
| certification | 13.70 | 0 | 0 | 0 |
| recovery | 187.80 | 121,234 | 12,401 | 36 |
| **total** | **201.50** | **121,234** | **12,401** | **36** |

## Tokens & cost

- total tokens: 133,635  (input 121,234 / output 12,401)
- LLM calls: 36
- estimated cost: $0.0000

## Generated code

- language: Python
- files: 12 · lines of code: 733
- files per layer: {'controller': 10, 'model': 1, 'view': 1}
- tech stack: F3__2__REQ__10Domain, F3__2__REQ__11Domain, F3__2__REQ__12Domain, F3__2__REQ__5Domain, F3__2__REQ__6Domain, F3__2__REQ__7Domain, F3__2__REQ__8Domain, F3__2__REQ__9Domain, app, dafny_marshal, fastapi, pydantic, sqlalchemy

## Generated tests

- features: 12 · test cases: 46

## Certification (pass@k)

- samples n=1
- pass@1: 0.000
- case pass rate: 0.000

## Recovery loop (re-prove + test-informed regen)

- passes run: 2 / 2 max
- re-proved (now ship from Dafny): ['3.2.REQ-1', '3.2.REQ-3']
- repaired with test feedback (clean-room relaxed): (none)
- still UNCERTIFIED: ['3.2.REQ-2', '3.2.REQ-4']

Final per-feature certification label:
  - 3.2.REQ-1: PROVED (recovery)
  - 3.2.REQ-10: PROVED
  - 3.2.REQ-11: PROVED
  - 3.2.REQ-12: PROVED
  - 3.2.REQ-2: UNCERTIFIED
  - 3.2.REQ-3: PROVED (recovery)
  - 3.2.REQ-4: UNCERTIFIED
  - 3.2.REQ-5: PROVED
  - 3.2.REQ-6: PROVED
  - 3.2.REQ-7: PROVED
  - 3.2.REQ-8: PROVED
  - 3.2.REQ-9: PROVED

## Dafny proof tier (formal verification)

- model: Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8
- features: 12 · proved: 8 · rate: 0.667
  - 3.2.REQ-1 (F3_2_REQ_1): unproved (→ test track) (6r)
  - 3.2.REQ-10 (F3_2_REQ_10): PROVED (1r)
  - 3.2.REQ-11 (F3_2_REQ_11): PROVED (1r)
  - 3.2.REQ-12 (F3_2_REQ_12): PROVED (1r)
  - 3.2.REQ-2 (F3_2_REQ_2): unproved (→ test track) (6r)
  - 3.2.REQ-3 (F3_2_REQ_3): unproved (→ test track) (6r)
  - 3.2.REQ-4 (F3_2_REQ_4): unproved (→ test track) (6r)
  - 3.2.REQ-5 (F3_2_REQ_5): PROVED (1r)
  - 3.2.REQ-6 (F3_2_REQ_6): PROVED (1r)
  - 3.2.REQ-7 (F3_2_REQ_7): PROVED (1r)
  - 3.2.REQ-8 (F3_2_REQ_8): PROVED (1r)
  - 3.2.REQ-9 (F3_2_REQ_9): PROVED (2r)

## Native compile (dafny translate py)

- compiled: 8 · failed: 4
