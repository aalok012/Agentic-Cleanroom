# API Usage Log

Track OpenAI **token consumption** and **LLM call counts** for the shared professor API key.
Updated automatically at the end of each `run_pipeline.py` invocation (including failed runs).

## Cumulative totals

| metric | value |
|---|---:|
| runs logged | 1 |
| LLM calls | 65 |
| input tokens | 128,053 |
| output tokens | 251,149 |
| total tokens | 379,202 |
| estimated cost (USD) | $0.1699 |

## Run history

| date (UTC) | run_id | status | SRS | model | calls | input tok | output tok | total tok | cost (USD) | seconds | result |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-06-24 20:34:22 | `20260624-203421-dineout-srs` | complete | dineout_srs.xml | openai/gpt-4.1-2025-04-14+openai/gpt-4o-mini | 99 | 244,137 | 52,675 | 296,812 | $0.5918 | 660.9 | [detail](outputs/runs/20260624-203421-dineout-srs.md) |
| 2026-06-25 05:00:33 | `20260625-050033-dineout-srs` | complete | dineout_srs.xml | openai/gpt-4.1-2025-04-14+openai/gpt-4o-mini | 82 | 231,159 | 45,971 | 277,130 | $0.6050 | 702.7 | [detail](outputs/runs/20260625-050033-dineout-srs.md) |
| 2026-06-25 07:50:12 | `20260625-075012-dineout-srs` | failed | dineout_srs.xml | openai/gpt-oss-120b | 2 | 1,755 | 2,533 | 4,288 | $0.0018 | 0.0 | [detail](outputs/runs/20260625-075012-dineout-srs.md) |
| 2026-06-25 08:33:56 | `20260625-083356-dineout-srs` | complete | dineout_srs.xml | anthropic/claude-4.6-sonnet-20260217 | 69 | 244,922 | 118,552 | 363,474 | $0.1079 | 1541.0 | [detail](outputs/runs/20260625-083356-dineout-srs.md) |
| 2026-06-25 09:00:17 | `20260625-090017-dineout-srs` | failed | dineout_srs.xml | deepseek/deepseek-chat-v3 | 1 | 1,118 | 835 | 1,953 | $0.0007 | 0.0 | [detail](outputs/runs/20260625-090017-dineout-srs.md) |
| 2026-06-25 09:05:05 | `20260625-090505-dineout-srs` | failed | dineout_srs.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 | [detail](outputs/runs/20260625-090505-dineout-srs.md) |
| 2026-06-25 09:05:29 | `20260625-090529-dineout-srs` | failed | dineout_srs.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 | [detail](outputs/runs/20260625-090529-dineout-srs.md) |
| 2026-06-25 09:13:54 | `20260625-091354-dineout-srs` | failed | dineout_srs.xml | deepseek/deepseek-chat-v3 | 12 | 13,824 | 3,225 | 17,049 | $0.0040 | 0.0 | [detail](outputs/runs/20260625-091354-dineout-srs.md) |
| 2026-06-25 09:17:55 | `20260625-091755-dineout-srs` | failed | dineout_srs.xml | deepseek/deepseek-chat-v3 | 9 | 10,605 | 2,555 | 13,160 | $0.0031 | 0.0 | [detail](outputs/runs/20260625-091755-dineout-srs.md) |
| 2026-06-25 09:20:03 | `20260625-092003-dineout-srs` | failed | dineout_srs.xml | deepseek/deepseek-chat-v3 | 4 | 4,781 | 1,025 | 5,806 | $0.0013 | 0.0 | [detail](outputs/runs/20260625-092003-dineout-srs.md) |
| 2026-06-25 19:20:00 | `20260625-192000-dineout-srs` | failed | dineout_srs.xml | anthropic/claude-4.6-sonnet-20260217 | 20 | 29,756 | 7,572 | 37,328 | $0.0090 | 0.0 | [detail](outputs/parallel/anthropic_claude-sonnet-4-6/runs/20260625-192000-dineout-srs.md) |
| 2026-06-25 21:08:21 | `20260625-210821-dineout-srs` | complete | dineout_srs.xml | openai/gpt-5.5-20260423 | 62 | 127,394 | 141,647 | 269,041 | $0.1041 | 2456.9 | [detail](outputs/parallel/openai_gpt-5_5/runs/20260625-210821-dineout-srs.md) |
| 2026-06-25 23:20:50 | `20260625-232050-dineout-srs` | complete | dineout_srs.xml | deepseek/deepseek-v4-pro-20260423 | 70 | 205,557 | 328,104 | 533,661 | $0.2277 | 6155.8 | [detail](outputs/parallel/deepseek_deepseek-v4-pro/runs/20260625-232050-dineout-srs.md) |
| 2026-06-26 03:30:30 | `20260626-033030-dineout-srs` | failed | dineout_srs.xml | openai/gpt-4.1-2025-04-14+openai/gpt-4o-mini+qwen/qwen3-max | 178 | 726,018 | 165,255 | 891,273 | $1.6048 | 0.0 | [detail](outputs/parallel/qwen_qwen3-max/runs/20260626-033030-dineout-srs.md) |
| 2026-06-26 05:00:29 | `20260626-050029-dineout-srs` | complete | dineout_srs.xml | google/gemini-3.1-pro-preview-20260219 | 65 | 128,053 | 251,149 | 379,202 | $0.1699 | 1912.6 | [detail](outputs/parallel/google_gemini-3_1-pro-preview/runs/20260626-050029-dineout-srs.md) |

## Notes

- Costs use `src/cleanroom/utils/cost.py` list prices for the reported model.
- `status=failed` means the pipeline exited early; tokens from completed stages are still counted.
- **Per-run detail** (config, pass@k, stage breakdown): `outputs/runs/<run_id>.md` and the cumulative index [RUN_RESULTS.md](RUN_RESULTS.md).
- Latest per-SRS snapshot (overwritten): `outputs/<srs>_run_report.md`.
