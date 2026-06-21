# API Usage Log

Track OpenAI **token consumption** and **LLM call counts** for the shared professor API key.
Updated automatically at the end of each `run_pipeline.py` invocation (including failed runs).

## Cumulative totals

| metric | value |
|---|---:|
| runs logged | 1 |
| LLM calls | 57 |
| input tokens | 176,377 |
| output tokens | 31,407 |
| total tokens | 207,784 |
| estimated cost (USD) | $0.6040 |

## Run history

| date (UTC) | run_id | status | SRS | model | calls | input tok | output tok | total tok | cost (USD) | seconds | result |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-06-21 07:49:09 | `spike-4.1-gpt-4o-mini` | spike-estimate (unverified 5r) | spike:4.1 | gpt-4o-mini | 5 | 18,115 | 3,500 | 21,615 | $0.0048 | 0.0 | - |
| 2026-06-21 07:49:09 | `spike-4.1-gpt-4o` | spike-estimate (verified 4r) | spike:4.1 | gpt-4o | 4 | 12,852 | 2,800 | 15,652 | $0.0036 | 0.0 | - |
| 2026-06-21 07:49:09 | `spike-4.10-gpt-4o` | spike-estimate (unverified 6r) | spike:4.10 | gpt-4o | 6 | 24,198 | 4,200 | 28,398 | $0.0062 | 0.0 | - |
| 2026-06-21 07:49:09 | `spike-4.10-gpt-4o` | spike-estimate (unverified 6r) | spike:4.10 | gpt-4o | 6 | 24,198 | 4,200 | 28,398 | $0.0062 | 0.0 | - |
| 2026-06-21 07:49:09 | `spike-4.10-gpt-4.1` | spike-estimate (verified 2r) | spike:4.10 | gpt-4.1 | 2 | 4,786 | 1,400 | 6,186 | $0.0016 | 0.0 | - |
| 2026-06-21 08:14:22 | `20260621-081422-dineout-srs` | complete | dineout_srs.xml | gpt-4.1-2025-04-14 | 71 | 233,554 | 43,093 | 276,647 | $0.8119 | 273.0 | [detail](outputs/runs/20260621-081422-dineout-srs.md) |
| 2026-06-21 18:30:31 | `spike-4.3-gpt-4.1-20260621-183031` | spike-unverified (6r) | spike:4.3 | gpt-4.1-2025-04-14 | 6 | 26,072 | 4,237 | 30,309 | $0.0860 | 0.0 | - |
| 2026-06-21 18:30:58 | `spike-4.4-gpt-4.1-20260621-183058` | spike-verified (5r) | spike:4.4 | gpt-4.1-2025-04-14 | 5 | 20,214 | 3,750 | 23,964 | $0.0704 | 0.0 | - |
| 2026-06-21 18:31:33 | `spike-4.6-gpt-4.1-20260621-183133` | spike-unverified (6r) | spike:4.6 | gpt-4.1-2025-04-14 | 6 | 29,890 | 5,588 | 35,478 | $0.1045 | 0.0 | - |
| 2026-06-21 18:33:10 | `spike-4.6-gpt-4.1-20260621-183310` | spike-unverified (7r) | spike:4.6 | gpt-4.1-2025-04-14 | 7 | 41,664 | 7,462 | 49,126 | $0.1430 | 0.0 | - |
| 2026-06-21 19:13:52 | `20260621-191352-dineout-srs` | complete | dineout_srs.xml | gpt-4.1-2025-04-14 | 57 | 176,377 | 31,407 | 207,784 | $0.6040 | 223.8 | [detail](outputs/runs/20260621-191352-dineout-srs.md) |

## Notes

- Costs use `src/cleanroom/utils/cost.py` list prices for the reported model.
- `status=failed` means the pipeline exited early; tokens from completed stages are still counted.
- **Per-run detail** (config, pass@k, stage breakdown): `outputs/runs/<run_id>.md` and the cumulative index [RUN_RESULTS.md](RUN_RESULTS.md).
- Latest per-SRS snapshot (overwritten): `outputs/<srs>_run_report.md`.
