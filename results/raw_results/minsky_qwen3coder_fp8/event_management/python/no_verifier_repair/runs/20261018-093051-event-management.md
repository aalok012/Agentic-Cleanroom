# Pipeline run `20261018-093051-event-management`

_Status: **complete** · 2026-10-18 09:30:51 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 221.8s
- **tokens**: 90,676 (in 69,821 / out 20,855)
- **LLM calls**: 36
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 742
- layers: {'controller': 10, 'model': 1, 'view': 1}

## Generated tests

- features: 12 · cases: 49

## Dafny proof tier

- proved: 8/12 · rate: 0.667

## Certification (pass@k)

- samples n=1
- **pass@1**: 0.000
- **case pass rate**: 0.000

## Per-stage timing & tokens

| stage | seconds | input tok | output tok | calls |
|---|---:|---:|---:|---:|
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 46.13 | 28,059 | 3,055 | 12 |
| compile | 8.94 | 0 | 0 | 0 |
| adapter | 5.57 | 1,542 | 644 | 1 |
| adapter | 5.23 | 1,548 | 606 | 1 |
| adapter | 5.28 | 1,478 | 609 | 1 |
| adapter | 5.41 | 1,523 | 624 | 1 |
| adapter | 4.62 | 1,592 | 529 | 1 |
| adapter | 7.37 | 1,585 | 854 | 1 |
| adapter | 6.14 | 1,638 | 708 | 1 |
| adapter | 5.83 | 1,573 | 672 | 1 |
| code | 12.14 | 4,793 | 1,417 | 4 |
| test | 95.89 | 24,490 | 11,137 | 12 |
| certification | 13.31 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/no_verifier_repair/runs/20261018-093051-event-management.json`
