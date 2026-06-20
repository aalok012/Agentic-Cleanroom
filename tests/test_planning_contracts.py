"""Unit tests for deterministic planning contract normalization."""

import json

from src.cleanroom.agents.planning.agent import (
    Contract,
    _align_kwargs_json,
    _dedupe_file_paths,
    _parse_signature_params,
)
from src.cleanroom.agents.spec_agent.schema.ir import BehavioralContract


def test_parse_signature_params():
    sig = "def update_torrent_database(request: dict) -> bool:"
    assert _parse_signature_params(sig) == ["request"]
    assert _parse_signature_params("def sort_search_results(criteria: str) -> list[dict[str, str]]:") == ["criteria"]


def test_align_wraps_flat_dict_for_single_request_param():
    sig = "def update_torrent_database(request: dict) -> bool:"
    aligned = _align_kwargs_json(sig, '{"update": true}')
    assert json.loads(aligned) == {"request": {"update": True}}


def test_align_leaves_matching_kwargs():
    sig = "def sort_search_results(criteria: str) -> list[dict[str, str]]:"
    raw = '{"criteria": "size"}'
    assert json.loads(_align_kwargs_json(sig, raw)) == json.loads(raw)


def test_align_leaves_nested_request():
    sig = "def update_video_database(request: dict) -> bool:"
    raw = '{"request": {"auth_token": "valid_token", "update_info": {"new_sites": ["a"]}}}'
    assert json.loads(_align_kwargs_json(sig, raw)) == json.loads(raw)


def test_dedupe_file_paths():
    bc = BehavioralContract(
        fr_id="x",
        feature_id="3.2",
        stimulus="s",
        precondition="none",
        response="r",
        postcondition="none",
    )
    contracts = [
        Contract(
            fr_id="3.1.REQ-6",
            feature_id="3.1",
            signature="def sort_search_results(criteria: str) -> list[dict[str, str]]:",
            docstring="doc",
            mvc_layer="controller",
            file_path="controllers/sort_search_results.py",
            contract=bc,
        ),
        Contract(
            fr_id="3.2.REQ-8",
            feature_id="3.2",
            signature="def sort_search_results(order_by: str) -> list[dict[str, str]]:",
            docstring="doc",
            mvc_layer="controller",
            file_path="controllers/sort_search_results.py",
            contract=bc,
        ),
    ]
    _dedupe_file_paths(contracts)
    paths = [c.file_path for c in contracts]
    assert len(set(paths)) == 2
    assert paths[0] == "controllers/sort_search_results.py"
    assert "3_2_REQ_8" in paths[1]
