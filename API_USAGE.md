# API Usage Log

Track OpenAI **token consumption** and **LLM call counts** for the shared professor API key.
Updated automatically at the end of each `run_pipeline.py` invocation (including failed runs).

## Cumulative totals

| metric | value |
|---|---:|
| runs logged | 1 |
| LLM calls | 146 |
| input tokens | 465,060 |
| output tokens | 90,417 |
| total tokens | 555,477 |
| estimated cost (USD) | $1.3200 |

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
| 2026-06-22 05:06:38 | `20260622-050638-dineout-srs` | complete | dineout_srs.xml | gpt-4.1-2025-04-14+gpt-4o-mini-2024-07-18 | 84 | 203,160 | 54,172 | 257,332 | $0.6249 | 659.3 | [detail](outputs/runs/20260622-050638-dineout-srs.md) |
| 2026-06-22 05:45:39 | `recertify-dineout_srs_full_ir` | recertify | dineout_srs_full_ir.json | none (free re-cert) | 0 | 0 | 0 | 0 | $0.0000 | 0.0 | - |
| 2026-06-22 05:52:24 | `recertify-dineout_srs_full_ir-n4` | recertify@4 | dineout_srs_full_ir.json | gpt-4o-mini-2024-07-18 | 30 | 31,638 | 9,796 | 41,434 | $0.0106 | 0.0 | - |
| 2026-06-23 03:50:15 | `reprove-dineout_srs_full_ir` | reprove | dineout_srs_full_ir.json | gpt-4.1-2025-04-14 | 21 | 111,123 | 23,343 | 134,466 | $0.4090 | 0.0 | - |
| 2026-06-23 04:08:51 | `20260623-040851-dineout-srs` | complete | dineout_srs.xml | gpt-4.1-2025-04-14+gpt-4o-mini-2024-07-18 | 86 | 248,201 | 59,416 | 307,617 | $0.7630 | 900.2 | [detail](outputs/runs/20260623-040851-dineout-srs.md) |
| 2026-06-23 23:22:34 | `20260623-232234-gemini-code-1781976236207` | complete | gemini-code-1781976236207.xml | gpt-4.1-2025-04-14+gpt-4o-mini-2024-07-18 | 20 | 58,970 | 10,008 | 68,978 | $0.1568 | 144.5 | [detail](outputs/runs/20260623-232234-gemini-code-1781976236207.md) |
| 2026-06-23 23:27:20 | `20260623-232720-2009-video-search` | complete | 2009 - video search.xml | gpt-4.1-2025-04-14+gpt-4o-mini-2024-07-18 | 17 | 78,228 | 23,551 | 101,779 | $0.2862 | 208.8 | [detail](outputs/runs/20260623-232720-2009-video-search.md) |
| 2026-06-24 05:09:40 | `20260624-050940-dineout-srs` | failed | dineout_srs.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 | [detail](outputs/runs/20260624-050940-dineout-srs.md) |
| 2026-06-24 05:13:04 | `20260624-051304-dineout-srs` | failed | dineout_srs.xml | gpt-4o-mini | 0 | 0 | 0 | 0 | $0.0000 | 0.0 | [detail](outputs/runs/20260624-051304-dineout-srs.md) |
| 2026-06-24 05:44:44 | `20260624-054444-dineout-srs` | complete | dineout_srs.xml | gpt-4.1-2025-04-14+gpt-4o-mini-2024-07-18 | 146 | 465,060 | 90,417 | 555,477 | $1.3200 | 1494.2 | [detail](outputs/runs/20260624-054444-dineout-srs.md) |

## Notes

- Costs use `src/cleanroom/utils/cost.py` list prices for the reported model.
- `status=failed` means the pipeline exited early; tokens from completed stages are still counted.
- **Per-run detail** (config, pass@k, stage breakdown): `outputs/runs/<run_id>.md` and the cumulative index [RUN_RESULTS.md](RUN_RESULTS.md).
- Latest per-SRS snapshot (overwritten): `outputs/<srs>_run_report.md`.
