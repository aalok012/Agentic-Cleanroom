"""Spec-derived pytest module for feature 4.15.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_get_help_overview():
    resp = client.post("/views/get_help_overview", json={})
    assert resp.status_code == 200
    assert resp.json() == {
        "operations": [
            {"name": "view_overview", "description": "Display help overview"},
            {"name": "select_operation", "description": "Select an operation by name"},
            {"name": "view_operation_details", "description": "View detailed info for a selected operation"}
        ]
    }

def test_select_help_operation_success():
    resp = client.post("/controllers/select_help_operation", json={"operation_name": "view_overview"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "selected_operation": "view_overview"}

def test_select_help_operation_failure():
    resp = client.post("/controllers/select_help_operation", json={"operation_name": "nonexistent_operation"})
    assert resp.status_code >= 400

def test_get_operation_details_success():
    # First select the operation
    client.post("/controllers/select_help_operation", json={"operation_name": "view_overview"})
    
    # Now get its details
    resp = client.post("/views/get_operation_details", json={"operation_name": "view_overview"})
    assert resp.status_code == 200
    assert resp.json() == {"operation": "view_overview", "details": "Display help overview"}

def test_get_operation_details_failure():
    resp = client.post("/views/get_operation_details", json={"operation_name": "nonexistent_operation"})
    assert resp.status_code >= 400
