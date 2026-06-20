"""Tests for per-run records and API usage log updates."""

import json
from pathlib import Path

from src.cleanroom.utils.run_record import (
    append_run_results_index,
    make_run_id,
    record_run,
    write_run_record,
)
from src.cleanroom.utils.usage_log import append_usage_log


def test_make_run_id_is_sortable():
    rid = make_run_id("2009 - video search.xml")
    assert rid.endswith("-2009-video-search") or "-video-search" in rid
    assert rid[:8].isdigit()


def test_write_run_record_creates_md_and_json(tmp_path: Path):
    metrics = {
        "srs": "demo.xml",
        "stack": "python",
        "model": "gpt-4o-mini",
        "total_seconds": 12.5,
        "cost_usd": 0.01,
        "tokens": {"input": 100, "output": 50, "total": 150, "calls": 3},
        "config": {"certify": True, "samples": 1, "verify": False},
        "stages": [{"name": "spec_parse", "seconds": 1.0, "input_tokens": 0, "output_tokens": 0, "calls": 0}],
        "certification": {"n": 1, "aggregate_pass_at": {"pass@1": 1.0}, "aggregate_case_pass_rate": 1.0},
    }
    run_id = "20260101-120000-demo"
    md_path, json_path = write_run_record(metrics, status="complete", run_id=run_id, runs_dir=tmp_path)
    assert md_path.exists()
    assert json_path.exists()
    payload = json.loads(json_path.read_text())
    assert payload["run_id"] == run_id
    assert payload["certification"]["aggregate_case_pass_rate"] == 1.0
    assert "pass@1" in md_path.read_text()


def test_record_run_updates_index(tmp_path: Path):
    runs_dir = tmp_path / "runs"
    index_path = tmp_path / "RUN_RESULTS.md"
    metrics = {
        "srs": "demo.xml",
        "stack": "python",
        "model": "gpt-4o-mini",
        "total_seconds": 5.0,
        "cost_usd": 0.001,
        "tokens": {"input": 10, "output": 5, "total": 15, "calls": 1},
        "config": {"certify": False},
        "stages": [],
    }
    out = record_run(metrics, status="complete", runs_dir=runs_dir, index_path=index_path, run_id="run-a")
    assert index_path.exists()
    text = index_path.read_text()
    assert "run-a" in text
    assert "demo.xml" in text
    assert out["markdown"].exists()


def test_append_usage_log_includes_run_id_and_link(tmp_path: Path):
    usage_path = tmp_path / "API_USAGE.md"
    result_path = tmp_path / "runs" / "run-a.md"
    result_path.parent.mkdir(parents=True)
    result_path.write_text("# run\n")
    metrics = {
        "srs": "demo.xml",
        "stack": "python",
        "model": "gpt-4o-mini",
        "total_seconds": 1.0,
        "cost_usd": 0.0001,
        "tokens": {"input": 1, "output": 1, "total": 2, "calls": 1},
        "run_id": "run-a",
    }
    append_usage_log(metrics, path=usage_path, status="complete", run_id="run-a", result_path=result_path)
    text = usage_path.read_text()
    assert "`run-a`" in text
    assert "runs/run-a.md" in text
    assert "RUN_RESULTS.md" in text
