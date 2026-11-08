"""Spec-derived pytest module for feature 3.2.REQ-7.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_manage_data_workflow_step_anchor_case():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"enter","data":{"title":"Sample Entry","content":"This is sample content."}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "organize", "message": "Data entered successfully. Proceed to organize the data."}

def test_manage_data_workflow_step_organize_step():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"organize","data":{"title":"Sample Entry","content":"This is sample content."}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "retrieve", "message": "Data organized successfully. Proceed to retrieve the data."}

def test_manage_data_workflow_step_retrieve_step():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"retrieve","data":{"title":"Sample Entry","content":"This is sample content."}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "modify", "message": "Data retrieved successfully. Proceed to modify the data."}

def test_manage_data_workflow_step_modify_step():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"modify","data":{"title":"Sample Entry","content":"Updated content."}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "delete", "message": "Data modified successfully. Proceed to delete the data."}

def test_manage_data_workflow_step_delete_step():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"delete","data":{"title":"Sample Entry","content":"Updated content."}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "completed", "message": "Data deleted successfully. Workflow completed."}

def test_manage_data_workflow_step_invalid_action():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"invalid_action","data":{"title":"Sample Entry","content":"This is sample content."}})
    assert resp.status_code >= 400
