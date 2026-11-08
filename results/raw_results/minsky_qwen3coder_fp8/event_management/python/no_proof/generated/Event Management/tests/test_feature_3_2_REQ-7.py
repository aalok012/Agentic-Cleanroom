"""Spec-derived pytest module for feature 3.2.REQ-7.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_execute_workflow_step_anchor_case():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"enter","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "organize", "message": "Item entered successfully. Please organize the item."}

def test_execute_workflow_step_organize_step():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"organize","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "retrieve", "message": "Item organized successfully. Please retrieve the item."}

def test_execute_workflow_step_retrieve_step():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"retrieve","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "modify", "message": "Item retrieved successfully. Please modify the item."}

def test_execute_workflow_step_modify_step():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"modify","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "delete", "message": "Item modified successfully. Please delete the item."}

def test_execute_workflow_step_delete_step():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"delete","data":{"item_name":"New Item","category":"Electronics"}})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Item deleted successfully. Process completed."}

def test_execute_workflow_step_invalid_step():
    resp = client.post("/controllers/execute_workflow_step", json={"step_type":"invalid_step","data":{}})
    assert resp.status_code >= 400
