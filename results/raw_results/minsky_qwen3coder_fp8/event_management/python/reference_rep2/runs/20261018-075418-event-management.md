# Pipeline run `20261018-075418-event-management`

_Status: **complete** · 2026-10-18 07:54:18 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 365.9s
- **tokens**: 227,094 (in 194,204 / out 32,890)
- **LLM calls**: 83
- **estimated cost**: $0.0000

## Generated code

- files: 12 · LOC: 775
- layers: {'controller': 10, 'model': 2}

## Generated tests

- features: 12 · cases: 48

## Dafny proof tier

- proved: 8/12 · rate: 0.667

## Certification (pass@k)

- samples n=1
- **pass@1**: 0.000
- **case pass rate**: 0.000

## Per-stage timing & tokens

| stage | seconds | input tok | output tok | calls |
|---|---:|---:|---:|---:|
| spec_parse | 0.01 | 0 | 0 | 0 |
| spec_contracts | 10.03 | 11,400 | 1,114 | 12 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 21.13 | 29,368 | 2,373 | 12 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 149.30 | 111,266 | 10,739 | 35 |
| compile | 8.78 | 0 | 0 | 0 |
| adapter | 5.54 | 1,484 | 642 | 1 |
| adapter | 4.93 | 1,538 | 568 | 1 |
| adapter | 4.47 | 1,527 | 514 | 1 |
| adapter | 5.76 | 1,474 | 666 | 1 |
| adapter | 5.54 | 1,552 | 640 | 1 |
| adapter | 5.23 | 1,533 | 602 | 1 |
| adapter | 6.20 | 1,591 | 716 | 1 |
| adapter | 6.62 | 1,631 | 765 | 1 |
| code | 16.87 | 5,114 | 1,937 | 4 |
| test | 101.03 | 24,726 | 11,614 | 12 |
| certification | 14.44 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/reference_rep2/runs/20261018-075418-event-management.json`
