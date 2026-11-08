"""Spec-derived pytest module for feature 3.2.REQ-7.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_canonical_enter_case():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"enter","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "organize", "message": "Item entered successfully. Please organize the item."}

def test_missing_fields_enter_case():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"enter","data":{"category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "organize", "message": "Item entered successfully. Please organize the item."}

def test_invalid_step_case():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"invalid_step","data":{}})
    assert resp.status_code >= 400

def test_organize_step_case():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"organize","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "retrieve", "message": "Item organized successfully. Please retrieve the item."}

def test_retrieve_step_case():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"retrieve","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "modify", "message": "Item retrieved successfully. Please modify the item."}
