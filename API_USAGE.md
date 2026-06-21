# API Usage Log

Track OpenAI **token consumption** and **LLM call counts** for the shared professor API key.
Updated automatically at the end of each `run_pipeline.py` invocation (including failed runs).

## Cumulative totals

| metric | value |
|---|---:|
| runs logged | 1 |
| LLM calls | 72 |
| input tokens | 73,495 |
| output tokens | 24,787 |
| total tokens | 98,282 |
| estimated cost (USD) | $0.0259 |

## Run history

| date (UTC) | run_id | status | SRS | model | calls | input tok | output tok | total tok | cost (USD) | seconds | result |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-06-20 19:22:01 | failed | 2009 - video search.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 |
| 2026-06-20 20:15:29 | failed | 2009 - video search.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 |
| 2026-06-20 20:15:50 | failed | 2009 - video search.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 |
| 2026-06-20 20:20:14 | failed | 2009 - video search.xml | gpt-4o-mini-2024-07-18 | 6 | 5,110 | 2,204 | 7,314 | $0.0021 | 0.0 |
| 2026-06-20 20:23:14 | failed | 2009 - video search.xml | gpt-4o-mini-2024-07-18 | 12 | 11,621 | 4,154 | 15,775 | $0.0042 | 0.0 |
| 2026-06-20 20:32:51 | failed | 2009 - video search.xml | gpt-4o-mini-2024-07-18 | 12 | 11,793 | 4,957 | 16,750 | $0.0047 | 0.0 |
| 2026-06-20 20:39:17 | `20260620-203917-2009-video-search` | complete | 2009 - video search.xml | gpt-4o-mini-2024-07-18 | 11 | 10,685 | 4,452 | 15,137 | $0.0043 | 60.6 | [detail](outputs/runs/20260620-203917-2009-video-search.md) |
| 2026-06-20 20:43:17 | `20260620-204317-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 40,300 | 10,158 | 50,458 | $0.0121 | 154.1 | [detail](outputs/runs/20260620-204317-dineout-srs.md) |
| 2026-06-20 20:59:56 | `20260620-205956-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 44 | 45,935 | 12,585 | 58,520 | $0.0144 | 177.3 | [detail](outputs/runs/20260620-205956-dineout-srs.md) |
| 2026-06-20 21:10:34 | `20260620-211034-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 40,620 | 10,217 | 50,837 | $0.0122 | 149.5 | [detail](outputs/runs/20260620-211034-dineout-srs.md) |
| 2026-06-20 21:40:58 | `20260620-214058-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 39,963 | 9,361 | 49,324 | $0.0116 | 164.8 | [detail](outputs/runs/20260620-214058-dineout-srs.md) |
| 2026-06-20 21:49:49 | `20260620-214949-dineout-srs` | failed | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 30 | 28,711 | 5,630 | 34,341 | $0.0077 | 0.0 | [detail](outputs/runs/20260620-214949-dineout-srs.md) |
| 2026-06-20 22:02:27 | `20260620-220227-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 42,803 | 13,703 | 56,506 | $0.0146 | 230.9 | [detail](outputs/runs/20260620-220227-dineout-srs.md) |
| 2026-06-20 22:17:15 | `20260620-221715-dineout-srs` | failed | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 30 | 31,143 | 6,172 | 37,315 | $0.0084 | 0.0 | [detail](outputs/runs/20260620-221715-dineout-srs.md) |
| 2026-06-20 23:15:04 | `20260620-231504-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 43,067 | 13,319 | 56,386 | $0.0145 | 200.5 | [detail](outputs/runs/20260620-231504-dineout-srs.md) |
| 2026-06-20 23:51:32 | `20260620-235132-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 43,186 | 13,688 | 56,874 | $0.0147 | 204.0 | [detail](outputs/runs/20260620-235132-dineout-srs.md) |
| 2026-06-21 00:35:56 | `20260621-003556-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 43,042 | 13,024 | 56,066 | $0.0143 | 209.9 | [detail](outputs/runs/20260621-003556-dineout-srs.md) |
| 2026-06-21 01:50:58 | `20260621-015058-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 47,260 | 13,959 | 61,219 | $0.0155 | 202.7 | [detail](outputs/runs/20260621-015058-dineout-srs.md) |
| 2026-06-21 05:37:36 | `20260621-053736-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 40 | 50,527 | 13,915 | 64,442 | $0.0159 | 194.0 | [detail](outputs/runs/20260621-053736-dineout-srs.md) |
| 2026-06-21 05:47:49 | `20260621-054749-dineout-srs` | complete | dineout_srs.xml | gpt-4o-mini-2024-07-18 | 72 | 73,495 | 24,787 | 98,282 | $0.0259 | 422.7 | [detail](outputs/runs/20260621-054749-dineout-srs.md) |

## Notes

- Costs use `src/cleanroom/utils/cost.py` list prices for the reported model.
- `status=failed` means the pipeline exited early; tokens from completed stages are still counted.
- **Per-run detail** (config, pass@k, stage breakdown): `outputs/runs/<run_id>.md` and the cumulative index [RUN_RESULTS.md](RUN_RESULTS.md).
- Latest per-SRS snapshot (overwritten): `outputs/<srs>_run_report.md`.
