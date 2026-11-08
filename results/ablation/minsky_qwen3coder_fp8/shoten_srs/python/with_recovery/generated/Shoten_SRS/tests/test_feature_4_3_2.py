"""Spec-derived pytest module for feature 4.3.2.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_initiate_print_shop_search_anchor():
    resp = client.post("/controllers/initiate_print_shop_search", json={})
    assert resp.status_code == 200
    assert resp.json() is None

def test_initiate_print_shop_search_independent():
    resp = client.post("/controllers/initiate_print_shop_search", json={})
    assert resp.status_code == 200
    assert resp.json() is None

def test_get_print_shop_search_results_anchor():
    resp = client.post("/views/get_print_shop_search_results", json={})
    assert resp.status_code == 200
    expected = [
        {"name": "PrintHub", "opening_time": "09:00", "closing_time": "18:00", "rate_per_page": 0.1},
        {"name": "QuickCopy", "opening_time": "08:30", "closing_time": "20:00", "rate_per_page": 0.15}
    ]
    assert resp.json() == expected

def test_get_print_shop_search_results_empty():
    # No prior search initiated, so no results
    resp = client.post("/views/get_print_shop_search_results", json={})
    assert resp.status_code == 200
    assert resp.json() == []
