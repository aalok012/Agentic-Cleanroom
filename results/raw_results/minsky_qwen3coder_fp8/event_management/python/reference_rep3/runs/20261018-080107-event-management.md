# Pipeline run `20261018-080107-event-management`

_Status: **complete** · 2026-10-18 08:01:07 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 407.0s
- **tokens**: 255,479 (in 220,807 / out 34,672)
- **LLM calls**: 90
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 736
- layers: {'controller': 10, 'model': 2}

## Generated tests

- features: 12 · cases: 48

## Dafny proof tier

- proved: 6/12 · rate: 0.500

## Certification (pass@k)

- samples n=1
- **pass@1**: 0.000
- **case pass rate**: 0.000

## Per-stage timing & tokens

| stage | seconds | input tok | output tok | calls |
|---|---:|---:|---:|---:|
| spec_parse | 0.01 | 0 | 0 | 0 |
| spec_contracts | 10.05 | 11,400 | 1,114 | 12 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 21.20 | 29,368 | 2,383 | 12 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 185.56 | 138,322 | 12,679 | 42 |
| compile | 6.59 | 0 | 0 | 0 |
| adapter | 4.67 | 1,484 | 536 | 1 |
| adapter | 5.60 | 1,538 | 657 | 1 |
| adapter | 5.15 | 1,547 | 594 | 1 |
| adapter | 4.75 | 1,474 | 546 | 1 |
| adapter | 4.95 | 1,602 | 570 | 1 |
| adapter | 5.03 | 1,533 | 589 | 1 |
| code | 29.03 | 7,791 | 3,355 | 6 |
| test | 100.72 | 24,748 | 11,649 | 12 |
| certification | 23.69 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/reference_rep3/runs/20261018-080107-event-management.json`
