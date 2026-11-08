"""Spec-derived pytest module for feature 3.2.REQ-9.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_add_client_access():
    resp = client.post("/manage_client_access", json={"action": "AddClient", "client_id": "client_123"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Client client_123 add."}

def test_delete_client_access():
    # First add the client
    client.post("/manage_client_access", json={"action": "AddClient", "client_id": "client_123"})
    # Then delete it
    resp = client.post("/manage_client_access", json={"action": "RemoveClient", "client_id": "client_123"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Client client_123 remove."}

def test_invalid_action():
    resp = client.post("/manage_client_access", json={"action": "invalid_action", "client_id": "client_123"})
    assert resp.status_code >= 400

def test_remove_nonexistent_client():
    resp = client.post("/manage_client_access", json={"action": "RemoveClient", "client_id": "nonexistent_client"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Client nonexistent_client remove."}

def test_empty_client_id():
    resp = client.post("/manage_client_access", json={"action": "AddClient", "client_id": ""})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Client  add."}
