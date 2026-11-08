"""Spec-derived pytest module for feature 4.1.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_initiate_account_creation():
    resp = client.post("/controllers/initiate_account_creation", json={})
    assert resp.status_code == 200
    assert resp.json() is None

def test_collect_user_registration_info():
    resp = client.post("/controllers/collect_user_registration_info", json={"name":"John Doe","institute_roll_number":"123456","shop_id":"B001","mobile_number":"9876543210","email_id":"johndoe@example.com"})
    assert resp.status_code == 200
    assert resp.json() is None

def test_assign_username_and_request_password():
    resp = client.post("/controllers/assign_username_and_request_password", json={})
    assert resp.status_code == 200
    assert resp.json() == {"username": "johndoe123"}

def test_confirm_password_acceptability_success():
    resp = client.post("/controllers/confirm_password_acceptability", json={"password":"SecurePass123!"})
    assert resp.status_code == 200
    assert resp.json() is True

def test_confirm_password_acceptability_failure():
    resp = client.post("/controllers/confirm_password_acceptability", json={"password":"weakpass"})
    assert resp.status_code >= 400

def test_store_user_information():
    resp = client.post("/models/store_user_information", json={"username":"johndoe123","password":"SecurePass123!","name":"John Doe","institute_roll_number":"123456","shop_id":"B001","mobile_number":"9876543210","email_id":"johndoe@example.com"})
    assert resp.status_code == 200
    assert resp.json() is True
