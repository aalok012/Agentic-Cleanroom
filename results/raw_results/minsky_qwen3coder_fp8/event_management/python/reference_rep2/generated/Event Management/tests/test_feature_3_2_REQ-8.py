"""Spec-derived pytest module for feature 3.2.REQ-8.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_manage_admin_client_access():
    # Test case 1: Canonical case - Admin user views client data successfully
    resp = client.post("/controllers/manage_admin_client_access", json={"admin_user_id":"admin123","action":"view","client_data":{"client_id":"client456"}})
    assert resp.status_code == 200
    assert resp.json() == {"access_granted": True, "data": {"client_id": "client456", "name": "John Doe", "email": "john@example.com"}}

    # Test case 2: Admin user modifies client data
    client.post("/controllers/manage_admin_client_access", json={"action": "add", "client_data": {"client_id": "client456", "name": "John Doe", "email": "john@example.com"}})
    resp = client.post("/controllers/manage_admin_client_access", json={"admin_user_id":"admin123","action":"modify","client_data":{"client_id":"client456", "name":"Jane Smith", "email":"jane@example.com"}})
    assert resp.status_code == 200
    assert resp.json() == {"access_granted": True, "data": {"client_id": "client456", "name": "Jane Smith", "email": "jane@example.com"}}

    # Test case 3: Admin user attempts to access non-existent client
    resp = client.post("/controllers/manage_admin_client_access", json={"admin_user_id":"admin123","action":"view","client_data":{"client_id":"client999"}})
    assert resp.status_code >= 400

    # Test case 4: Empty admin user ID provided
    resp = client.post("/controllers/manage_admin_client_access", json={"admin_user_id":"","action":"view","client_data":{"client_id":"client456"}})
    assert resp.status_code >= 400

    # Test case 5: Invalid action type provided
    client.post("/controllers/manage_admin_client_access", json={"action": "add", "client_data": {"client_id": "client456", "name": "John Doe", "email": "john@example.com"}})
    resp = client.post("/controllers/manage_admin_client_access", json={"admin_user_id":"admin123","action":"delete","client_data":{"client_id":"client456"}})
    assert resp.status_code >= 400
