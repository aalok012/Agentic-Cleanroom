"""Spec-derived pytest module for feature 4.14.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_anchor_case_logout_logged_in_user():
    # Arrange: Login a user first
    login_response = client.post("/controllers/fr_4_14_REQ_1", json={"action": "login", "credentials": {"username": "testuser", "password": "password123"}})
    assert login_response.status_code == 200
    
    # Act: Logout the user
    resp = client.post("/controllers/fr_4_14_REQ_1", json={"request": {}})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == {}

def test_failure_case_not_logged_in():
    # Act: Try to logout without being logged in
    resp = client.post("/controllers/fr_4_14_REQ_1", json={"request": {}})
    
    # Assert
    assert resp.status_code >= 400

def test_failure_case_malformed_request():
    # Arrange: Login a user first
    login_response = client.post("/controllers/fr_4_14_REQ_1", json={"action": "login", "credentials": {"username": "testuser", "password": "password123"}})
    assert login_response.status_code == 200
    
    # Act: Logout with malformed request
    resp = client.post("/controllers/fr_4_14_REQ_1", json={"request": {"unexpected_field": "value"}})
    
    # Assert
    assert resp.status_code >= 400

def test_success_case_empty_request_body():
    # Arrange: Login a user first
    login_response = client.post("/controllers/fr_4_14_REQ_1", json={"action": "login", "credentials": {"username": "testuser", "password": "password123"}})
    assert login_response.status_code == 200
    
    # Act: Logout with empty request body
    resp = client.post("/controllers/fr_4_14_REQ_1", json={"request": {}})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == {}
