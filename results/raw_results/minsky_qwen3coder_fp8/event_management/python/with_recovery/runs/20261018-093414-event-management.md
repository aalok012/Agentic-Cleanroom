# Pipeline run `20261018-093414-event-management`

_Status: **complete** · 2026-10-18 09:34:14 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 201.5s
- **tokens**: 133,635 (in 121,234 / out 12,401)
- **LLM calls**: 36
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 733
- layers: {'controller': 10, 'model': 1, 'view': 1}

## Generated tests

- features: 12 · cases: 46

## Dafny proof tier

- proved: 8/12 · rate: 0.667

## Certification (pass@k)

- samples n=1
- **pass@1**: 0.000
- **case pass rate**: 0.000

## Per-stage timing & tokens

| stage | seconds | input tok | output tok | calls |
|---|---:|---:|---:|---:|
| certification | 13.70 | 0 | 0 | 0 |
| recovery | 187.80 | 121,234 | 12,401 | 36 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/with_recovery/runs/20261018-093414-event-management.json`
