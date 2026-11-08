# Pipeline run `20261018-091829-event-management`

_Status: **complete** · 2026-10-18 09:18:29 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 110.3s
- **tokens**: 41,281 (in 30,387 / out 10,894)
- **LLM calls**: 12
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 733
- layers: {'controller': 10, 'model': 1, 'view': 1}

## Generated tests

- features: 12 · cases: 47

## Dafny proof tier

- proved: 8/12 · rate: 0.667

## Certification (pass@k)

- samples n=1
- **pass@1**: 0.000
- **case pass rate**: 0.000

## Per-stage timing & tokens

| stage | seconds | input tok | output tok | calls |
|---|---:|---:|---:|---:|
| test | 95.75 | 30,387 | 10,894 | 12 |
| certification | 14.59 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/test_sees_code/runs/20261018-091829-event-management.json`
