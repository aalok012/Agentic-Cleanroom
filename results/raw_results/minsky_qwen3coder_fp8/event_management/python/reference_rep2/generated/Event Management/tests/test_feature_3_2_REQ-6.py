"""Spec-derived pytest module for feature 3.2.REQ-6.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_get_stakeholder_info_valid_id():
    resp = client.post("/models/get_stakeholder_info", json={"stakeholder_id":"stakeholder_123"})
    assert resp.status_code == 200
    assert resp.json() == {"login_credentials": "encrypted_login_data", "personal_details": "encrypted_personal_info"}

def test_get_stakeholder_info_empty_id():
    resp = client.post("/models/get_stakeholder_info", json={"stakeholder_id":""})
    assert resp.status_code >= 400

def test_get_stakeholder_info_nonexistent_id():
    resp = client.post("/models/get_stakeholder_info", json={"stakeholder_id":"non_existent_123"})
    assert resp.status_code >= 400

def test_get_stakeholder_info_special_chars_id():
    resp = client.post("/models/get_stakeholder_info", json={"stakeholder_id":"stakeholder_!@#$%^&*()"})
    assert resp.status_code == 200
    assert resp.json() == {"login_credentials": "encrypted_login_data", "personal_details": "encrypted_personal_info"}
