"""Spec-derived pytest module for feature 3.2.REQ-9.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_manage_client_access_add():
    resp = client.post("/controllers/manage_client_access", json={"action":"add","client_id":"client_123"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Client access added successfully"}

def test_manage_client_access_delete():
    # First add the client access
    client.post("/controllers/manage_client_access", json={"action":"add","client_id":"client_123"})
    
    # Then delete it
    resp = client.post("/controllers/manage_client_access", json={"action":"delete","client_id":"client_123"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Client access deleted successfully"}

def test_manage_client_access_invalid_action():
    resp = client.post("/controllers/manage_client_access", json={"action":"invalid_action","client_id":"client_123"})
    assert resp.status_code >= 400

def test_manage_client_access_delete_nonexistent():
    resp = client.post("/controllers/manage_client_access", json={"action":"delete","client_id":"nonexistent_client"})
    assert resp.status_code >= 400

def test_manage_client_access_empty_client_id():
    resp = client.post("/controllers/manage_client_access", json={"action":"add","client_id":""})
    assert resp.status_code >= 400
