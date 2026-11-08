# Pipeline run `20261018-092706-event-management`

_Status: **complete** · 2026-10-18 09:27:06 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 332.7s
- **tokens**: 220,574 (in 192,986 / out 27,588)
- **LLM calls**: 71
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 637
- layers: {'controller': 12}

## Generated tests

- features: 12 · cases: 47

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
| spec_contracts | 0.00 | 0 | 0 | 0 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 0.00 | 0 | 0 | 0 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 183.75 | 153,730 | 13,326 | 47 |
| compile | 6.45 | 0 | 0 | 0 |
| adapter | 5.77 | 1,506 | 667 | 1 |
| adapter | 5.70 | 1,517 | 658 | 1 |
| adapter | 4.96 | 1,487 | 572 | 1 |
| adapter | 6.33 | 1,705 | 729 | 1 |
| adapter | 5.18 | 1,505 | 594 | 1 |
| adapter | 5.69 | 1,508 | 656 | 1 |
| code | 15.93 | 6,388 | 1,800 | 6 |
| test | 74.91 | 23,640 | 8,586 | 12 |
| certification | 18.02 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/raw_spec_only/runs/20261018-092706-event-management.json`
