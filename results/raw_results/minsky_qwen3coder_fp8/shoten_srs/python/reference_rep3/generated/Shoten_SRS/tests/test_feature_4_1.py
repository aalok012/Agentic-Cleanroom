"""Spec-derived pytest module for feature 4.1.

Generated black-box from the specification (10 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_req_1_anchor():
    resp = client.post("/controllers/initiate_account_creation", json={"user_type":"student"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "account creation initiated"}

def test_req_1_failure():
    resp = client.post("/controllers/initiate_account_creation", json={"user_type":"invalid"})
    assert resp.status_code >= 400

def test_req_2_anchor():
    resp = client.post("/controllers/collect_user_information", json={"name":"John Doe","user_type":"student","roll_number":"12345","shop_id":"","mobile_number":"9876543210","email_id":"john.doe@example.com"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "information collected"}

def test_req_2_failure():
    resp = client.post("/controllers/collect_user_information", json={"name":"","user_type":"student","roll_number":"12345","shop_id":"","mobile_number":"9876543210","email_id":"john.doe@example.com"})
    assert resp.status_code >= 400

def test_req_3_anchor():
    resp = client.post("/controllers/assign_username_and_prompt_password", json={"name":"John Doe","user_type":"student","roll_number":"12345","shop_id":"","mobile_number":"9876543210","email_id":"john.doe@example.com"})
    assert resp.status_code == 200
    assert resp.json() == {"username": "johndoe123", "prompt": "Please set a password"}

def test_req_3_failure():
    resp = client.post("/controllers/assign_username_and_prompt_password", json={"name":"","user_type":"student","roll_number":"12345","shop_id":"","mobile_number":"9876543210","email_id":"john.doe@example.com"})
    assert resp.status_code >= 400

def test_req_4_anchor():
    resp = client.post("/controllers/confirm_password_acceptability", json={"password":"SecurePass123!"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_req_4_failure():
    resp = client.post("/controllers/confirm_password_acceptability", json={"password":"123"})
    assert resp.status_code >= 400

def test_req_5_anchor():
    resp = client.post("/models/store_user_information", json={"username":"johndoe123","password":"SecurePass123!","name":"John Doe","user_type":"student","roll_number":"12345","shop_id":"","mobile_number":"9876543210","email_id":"john.doe@example.com"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "user information stored"}

def test_req_5_failure():
    resp = client.post("/models/store_user_information", json={"username":"johndoe123","password":"123","name":"John Doe","user_type":"student","roll_number":"12345","shop_id":"","mobile_number":"9876543210","email_id":"john.doe@example.com"})
    assert resp.status_code >= 400
