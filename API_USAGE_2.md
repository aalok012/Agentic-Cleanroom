# API Usage Log

Track OpenAI **token consumption** and **LLM call counts** for the shared professor API key.
Updated automatically at the end of each `run_pipeline.py` invocation (including failed runs).

## Cumulative totals

| metric | value |
|---|---:|
| runs logged | 1 |
| LLM calls | 82 |
| input tokens | 231,159 |
| output tokens | 45,971 |
| total tokens | 277,130 |
| estimated cost (USD) | $0.6050 |

## Run history

| date (UTC) | run_id | status | SRS | model | calls | input tok | output tok | total tok | cost (USD) | seconds | result |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-06-24 20:34:22 | `20260624-203421-dineout-srs` | complete | dineout_srs.xml | openai/gpt-4.1-2025-04-14+openai/gpt-4o-mini | 99 | 244,137 | 52,675 | 296,812 | $0.5918 | 660.9 | [detail](outputs/runs/20260624-203421-dineout-srs.md) |
| 2026-06-25 05:00:33 | `20260625-050033-dineout-srs` | complete | dineout_srs.xml | openai/gpt-4.1-2025-04-14+openai/gpt-4o-mini | 82 | 231,159 | 45,971 | 277,130 | $0.6050 | 702.7 | [detail](outputs/runs/20260625-050033-dineout-srs.md) |

## Notes

- Costs use `src/cleanroom/utils/cost.py` list prices for the reported model.
- `status=failed` means the pipeline exited early; tokens from completed stages are still counted.
- **Per-run detail** (config, pass@k, stage breakdown): `outputs/runs/<run_id>.md` and the cumulative index [RUN_RESULTS.md](RUN_RESULTS.md).
- Latest per-SRS snapshot (overwritten): `outputs/<srs>_run_report.md`.
