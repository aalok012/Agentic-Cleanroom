"""Spec-derived pytest module for feature 3.2.REQ-7.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_manage_data_workflow_step_anchor_case():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"enter","data":{"title":"New Entry","content":"Some content"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "organize", "instructions": "Please organize the entered data by category"}

def test_manage_data_workflow_step_organize_case():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"organize","data":{"category":"Work"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "retrieve", "instructions": "Please retrieve the organized data"}

def test_manage_data_workflow_step_retrieve_case():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"retrieve","data":{"id":"1"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "modify", "instructions": "Please modify the retrieved data"}

def test_manage_data_workflow_step_modify_case():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"modify","data":{"id":"1","content":"Updated content"}})
    assert resp.status_code == 200
    assert resp.json() == {"next_step": "delete", "instructions": "Please delete the modified data"}

def test_manage_data_workflow_step_invalid_action():
    resp = client.post("/controllers/manage_data_workflow_step", json={"action":"invalid_action","data":{"title":"Test"}})
    assert resp.status_code >= 400
