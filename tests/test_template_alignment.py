"""Smoke tests: every agent prompt renders without UndefinedError."""

import pytest

from src.cleanroom.utils.prompt_renderer import PromptRenderer


@pytest.fixture
def renderer() -> PromptRenderer:
    return PromptRenderer()


def _prereq():
    return [{
        "fr_id": "3.1.REQ-2",
        "layer": "model",
        "signature": "def update_db(request: dict) -> bool:",
        "file_path": "models/update_db.py",
        "example_inputs_json": '{"request":{"update":true}}',
    }]


def test_generate_code_j2_python(renderer):
    out = renderer.render(
        "generate_code.j2",
        {
            "fr_id": "3.1.REQ-4",
            "feature_id": "3.1",
            "mvc_layer": "controller",
            "signature": "def foo(query: str) -> list[dict[str, str]]:",
            "docstring": "Doc.",
            "requirement": "Retrieve details.",
            "prerequisites": _prereq(),
            "stack": "python",
            "example_inputs_json": '{"query":"x"}',
            "expected_return_json": "[]",
            "error_mode": "raise",
            "failure_inputs_json": "",
        },
    )
    assert "plain, framework-free Python" in out
    assert "models/update_db.py" in out


def test_generate_code_j2_fastapi(renderer):
    out = renderer.render(
        "generate_code.j2",
        {
            "fr_id": "3.1.REQ-1",
            "feature_id": "3.1",
            "mvc_layer": "controller",
            "signature": "def search(q: str) -> dict:",
            "docstring": "Doc.",
            "requirement": "Search.",
            "prerequisites": [],
            "stack": "fastapi",
            "example_inputs_json": '{"q":"x"}',
            "expected_return_json": "{}",
            "error_mode": "raise",
            "failure_inputs_json": "",
            "entity_identifier": "id",
        },
    )
    assert "FastAPI" in out
    assert "look up the entity by its `id` field" in out


def test_generate_tests_j2(renderer):
    # Build the requirement through the real helper so the template and its inputs stay aligned.
    from src.cleanroom.utils.contracts import requirement_for_prompt

    req = requirement_for_prompt(
        {"id": "3.1.REQ-1", "text": "Search bar shared."},
        {
            "signature": "def search_torrents(query: str) -> dict:",
            "file_path": "controllers/search_torrents.py",
            "example_inputs_json": '{"query":"x"}',
            "expected_return_json": "{}",
            "failure_inputs_json": '{"query":""}',
            "error_mode": "raise",
            "contract": {"stimulus": "User searches.", "precondition": "none",
                         "response": "Results.", "postcondition": "none"},
        },
    )
    ctx = {"feature_id": "3.1", "name": "Torrent Search", "description": "Search torrents.",
           "requirements": [req]}

    py = renderer.render("generate_tests.j2", {**ctx, "stack": "python"})
    assert "3.1.REQ-1" in py and "Search bar shared." in py
    assert "pytest.raises(ValueError)" in py and "TestClient" not in py

    api = renderer.render("generate_tests.j2", {**ctx, "stack": "fastapi"})
    assert "POST /controllers/search_torrents" in api
    assert "TestClient" in api and "HTTPException" in api
    assert "pytest.raises(ValueError)" not in api


def test_plan_feature_j2(renderer):
    out = renderer.render(
        "plan_feature.j2",
        {
            "feature_name": "Torrent Search",
            "stack": "python",
            "requirements": [{
                "id": "3.1.REQ-1",
                "text": "Shared search bar.",
                "contract": {
                    "stimulus": "User types query",
                    "response": "Results returned",
                    "precondition": "none",
                    "postcondition": "none",
                },
            }],
        },
    )
    assert "plain Python" in out


def test_spec_reader_merges_planning():
    from src.cleanroom.agents.test.tools.spec_reader import feature_units

    ir = {
        "features": [{
            "id": "3.1",
            "name": "Torrent Search",
            "description": "desc",
            "functional_requirements": [{"id": "3.1.REQ-1", "text": "Shared search bar."}],
        }],
        "planning": {
            "contracts": [{
                "fr_id": "3.1.REQ-1",
                "signature": "def search_torrents(query: str) -> dict:",
                "file_path": "controllers/search_torrents.py",
                "example_inputs_json": '{"query":"x"}',
                "expected_return_json": "{}",
                "failure_inputs_json": "",
                "error_mode": "raise",
            }],
        },
    }
    unit = feature_units(ir)[0]
    req = unit["requirements"][0]
    assert req["text"] == "Shared search bar."
    assert req["file_path"] == "controllers/search_torrents.py"
    assert req["example_inputs_json"] == '{"query":"x"}'
