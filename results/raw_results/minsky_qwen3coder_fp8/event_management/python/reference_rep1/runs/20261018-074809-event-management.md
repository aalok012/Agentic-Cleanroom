# Pipeline run `20261018-074809-event-management`

_Status: **complete** · 2026-10-18 07:48:09 UTC_

## Configuration

- **SRS**: `Event Management.xml`
- **stack**: `fastapi`
- **model**: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- **flags**: certify=True (n=1), prove=True (target=py)

## Outcome

- **duration**: 338.4s
- **tokens**: 214,284 (in 185,528 / out 28,756)
- **LLM calls**: 81
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
| spec_parse | 0.01 | 0 | 0 | 0 |
| spec_contracts | 9.42 | 11,400 | 1,030 | 12 |
| dependency | 0.00 | 0 | 0 | 0 |
| planning | 18.59 | 29,339 | 2,060 | 12 |
| scaffold | 0.00 | 0 | 0 | 0 |
| dafny | 142.03 | 103,105 | 8,941 | 33 |
| compile | 8.93 | 0 | 0 | 0 |
| adapter | 5.34 | 1,537 | 618 | 1 |
| adapter | 4.92 | 1,548 | 567 | 1 |
| adapter | 5.25 | 1,478 | 607 | 1 |
| adapter | 4.84 | 1,519 | 558 | 1 |
| adapter | 3.21 | 1,514 | 363 | 1 |
| adapter | 7.10 | 1,585 | 822 | 1 |
| adapter | 6.10 | 1,648 | 704 | 1 |
| adapter | 6.27 | 1,572 | 726 | 1 |
| code | 12.64 | 4,793 | 1,437 | 4 |
| test | 89.89 | 24,490 | 10,323 | 12 |
| certification | 13.82 | 0 | 0 | 0 |

## Machine-readable

- JSON: `/home/cfw36/cleanroom_ablation_20261018/outputs/ablations/minsky_qwen3coder_fp8/event_management/python/reference_rep1/runs/20261018-074809-event-management.json`
