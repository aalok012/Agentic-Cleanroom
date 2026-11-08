# Pipeline run `20261018-092131-event-management`

_Status: **complete** · 2026-10-18 09:21:31 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=False (target=py)

## Outcome

- **duration**: 179.0s
- **tokens**: 53,876 (in 38,575 / out 15,301)
- **LLM calls**: 24
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 462
- layers: {'model': 4, 'controller': 6, 'view': 2}

## Generated tests

- features: 12 · cases: 50

## Certification (pass@k)

- samples n=1
- **pass@1**: 0.083
- **case pass rate**: 0.360

## Per-stage timing & tokens

| stage | seconds | input tok | output tok | calls |
|---|---:|---:|---:|---:|
| code | 33.94 | 14,085 | 3,846 | 12 |
| test | 98.85 | 24,490 | 11,455 | 12 |
| certification | 46.19 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/no_proof/runs/20261018-092131-event-management.json`
