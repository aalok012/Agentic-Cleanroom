# Pipeline Run Results

Paper-friendly index of every `run_pipeline.py` invocation. Each run has a dedicated markdown + JSON file under `outputs/runs/`.

| run_id | date (UTC) | status | SRS | stack | certify | pass@1 | case rate | tokens | cost (USD) | seconds | detail |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `20260621-191352-dineout-srs` | 2026-06-21 19:13:52 | complete | dineout_srs.xml | lemmafit | yes | - | - | 207,784 | $0.6040 | 223.8 | [20260621-191352-dineout-srs.md](outputs/runs/20260621-191352-dineout-srs.md) |
| `20260621-081422-dineout-srs` | 2026-06-21 08:14:22 | complete | dineout_srs.xml | lemmafit | yes | - | - | 276,647 | $0.8119 | 273.0 | [20260621-081422-dineout-srs.md](outputs/runs/20260621-081422-dineout-srs.md) |
| `20260621-054749-dineout-srs` | 2026-06-21 05:47:49 | complete | dineout_srs.xml | python | yes | 0.100 | 0.542 | 98,282 | $0.0259 | 422.7 | [20260621-054749-dineout-srs.md](outputs/runs/20260621-054749-dineout-srs.md) |
| `20260621-053736-dineout-srs` | 2026-06-21 05:37:36 | complete | dineout_srs.xml | fastapi | yes | 0.100 | 0.525 | 64,442 | $0.0159 | 194.0 | [20260621-053736-dineout-srs.md](outputs/runs/20260621-053736-dineout-srs.md) |
| `20260621-015058-dineout-srs` | 2026-06-21 01:50:58 | complete | dineout_srs.xml | fastapi | yes | 0.000 | 0.000 | 61,219 | $0.0155 | 202.7 | [20260621-015058-dineout-srs.md](outputs/runs/20260621-015058-dineout-srs.md) |
| `20260621-003556-dineout-srs` | 2026-06-21 00:35:56 | complete | dineout_srs.xml | fastapi | yes | 0.200 | 0.541 | 56,066 | $0.0143 | 209.9 | [20260621-003556-dineout-srs.md](outputs/runs/20260621-003556-dineout-srs.md) |
| `20260620-235132-dineout-srs` | 2026-06-20 23:51:32 | complete | dineout_srs.xml | fastapi | yes | 0.200 | 0.595 | 56,874 | $0.0147 | 204.0 | [20260620-235132-dineout-srs.md](outputs/runs/20260620-235132-dineout-srs.md) |
| `20260620-231504-dineout-srs` | 2026-06-20 23:15:04 | complete | dineout_srs.xml | fastapi | yes | 0.000 | 0.000 | 56,386 | $0.0145 | 200.5 | [20260620-231504-dineout-srs.md](outputs/runs/20260620-231504-dineout-srs.md) |
| `20260620-221715-dineout-srs` | 2026-06-20 22:17:15 | failed | dineout_srs.xml | fastapi | yes | - | - | 37,315 | $0.0084 | 0.0 | [20260620-221715-dineout-srs.md](outputs/runs/20260620-221715-dineout-srs.md) |
| `20260620-220227-dineout-srs` | 2026-06-20 22:02:27 | complete | dineout_srs.xml | fastapi | yes | 0.000 | 0.000 | 56,506 | $0.0146 | 230.9 | [20260620-220227-dineout-srs.md](outputs/runs/20260620-220227-dineout-srs.md) |
| `20260620-214949-dineout-srs` | 2026-06-20 21:49:49 | failed | dineout_srs.xml | python | yes | - | - | 34,341 | $0.0077 | 0.0 | [20260620-214949-dineout-srs.md](outputs/runs/20260620-214949-dineout-srs.md) |
| `20260620-214058-dineout-srs` | 2026-06-20 21:40:58 | complete | dineout_srs.xml | fastapi | yes | 0.000 | 0.000 | 49,324 | $0.0116 | 164.8 | [20260620-214058-dineout-srs.md](outputs/runs/20260620-214058-dineout-srs.md) |
| `20260620-211034-dineout-srs` | 2026-06-20 21:10:34 | complete | dineout_srs.xml | python | yes | 1.000 | 1.000 | 50,837 | $0.0122 | 149.5 | [20260620-211034-dineout-srs.md](outputs/runs/20260620-211034-dineout-srs.md) |
| `20260620-205956-dineout-srs` | 2026-06-20 20:59:56 | complete | dineout_srs.xml | python | yes | 0.700 | 0.833 | 58,520 | $0.0144 | 177.3 | [20260620-205956-dineout-srs.md](outputs/runs/20260620-205956-dineout-srs.md) |
| `20260620-204317-dineout-srs` | 2026-06-20 20:43:17 | complete | dineout_srs.xml | fastapi | yes | 0.000 | 0.000 | 50,458 | $0.0121 | 154.1 | [20260620-204317-dineout-srs.md](outputs/runs/20260620-204317-dineout-srs.md) |
| `20260620-203917-2009-video-search` | 2026-06-20 20:39:17 | complete | 2009 - video search.xml | python | yes | 1.000 | 1.000 | 15,137 | $0.0043 | 60.6 | [20260620-203917-2009-video-search.md](outputs/runs/20260620-203917-2009-video-search.md) |

## Notes

- Newest runs appear at the top of the table.
- Token/cost totals across all runs: see [API_USAGE.md](API_USAGE.md).
- Latest per-SRS artifacts (overwritten each run): `outputs/<srs>_full_ir.json`, `outputs/<srs>_run_report.md`.
