"""SPEC.yaml generation from IR behavioral contracts (LemmaFit TypeScript stack)."""

import yaml

from src.cleanroom.utils.lemmafit_spec import build_spec_entries, build_spec_yaml


def _ir() -> dict:
    return {
        "features": [{"id": "4.1", "name": "Place Order"}],
        "planning": {"contracts": [
            {
                "fr_id": "4.1.REQ-1", "feature_id": "4.1",
                "prerequisite_fr_ids": [],
                "contract": {
                    "stimulus": "Customer selects dishes",
                    "precondition": "the dish is available",
                    "response": "the order lists the selected dishes",
                    "postcondition": "order total equals the sum of dish prices",
                },
            },
            {
                "fr_id": "4.1.REQ-2", "feature_id": "4.1",
                "prerequisite_fr_ids": ["4.1.REQ-1"],
                "contract": {
                    "stimulus": "Customer confirms",
                    "precondition": "none",            # → no precondition entry
                    "response": "the order is placed",
                    "postcondition": "",               # falls back to response
                },
            },
        ]},
    }


def test_entries_shape_and_types():
    entries = build_spec_entries(_ir())
    # REQ-1: precondition + postcondition; REQ-2: postcondition only (precondition is "none").
    types = [e["type"] for e in entries]
    assert types == ["precondition", "postcondition", "postcondition"]
    assert all(e["verifiable"] and e["guarantee_type"] == "verified" for e in entries)
    assert all(e["state"] == "DRAFT" for e in entries)             # formalized later by Dafny stage
    assert all(e["module"] == "Core_4_1" for e in entries)          # valid Dafny module name
    assert len({e["id"] for e in entries}) == len(entries)          # unique ids
    assert all(e["req_id"].startswith("4.1.REQ-") for e in entries)


def test_postcondition_falls_back_to_response():
    entries = build_spec_entries(_ir())
    req2_post = next(e for e in entries if e["req_id"] == "4.1.REQ-2")
    assert req2_post["type"] == "postcondition"
    assert "the order is placed" in req2_post["property"]


def test_depends_on_links_prerequisite_postconditions():
    entries = build_spec_entries(_ir())
    req1_post = next(e for e in entries if e["req_id"] == "4.1.REQ-1" and e["type"] == "postcondition")
    req2_post = next(e for e in entries if e["req_id"] == "4.1.REQ-2")
    assert req2_post["depends_on"] == [req1_post["id"]]


def test_yaml_round_trips_and_is_valid():
    doc = yaml.safe_load(build_spec_yaml(_ir()))
    assert "entries" in doc and isinstance(doc["entries"], list)
    # YAML quotes properties with special characters so LemmaFit can parse them.
    assert doc["entries"][0]["property"]  # non-empty, parseable
