"""Spec-derived pytest module for feature 4.15.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_get_help_overview():
    resp = client.post("/views/get_help_overview", json={})
    assert resp.status_code == 200
    assert resp.json() == {
        "operations": [
            {"name": "order_food", "description": "Place a food order"},
            {"name": "view_menu", "description": "View available dishes"}
        ]
    }

def test_select_operation_success():
    resp = client.post("/controllers/select_operation", json={"operation_name": "order_food"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "selected", "operation": "order_food"}

def test_select_operation_failure():
    resp = client.post("/controllers/select_operation", json={"operation_name": "nonexistent_operation"})
    assert resp.status_code >= 400

def test_get_operation_details_success():
    # First select the operation
    client.post("/controllers/select_operation", json={"operation_name": "order_food"})
    
    # Now get the details
    resp = client.post("/views/get_operation_details", json={"operation_name": "order_food"})
    assert resp.status_code == 200
    assert resp.json() == {
        "operation": "order_food",
        "usage": "Send a POST request with dish names and quantities"
    }

def test_get_operation_details_failure():
    # Attempt to get details without selecting first
    resp = client.post("/views/get_operation_details", json={"operation_name": "order_food"})
    assert resp.status_code >= 400
