"""Spec-derived pytest module for feature 4.11.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_initiate_account_update_anchor():
    resp = client.post("/controllers/initiate_account_update", json={"user_id":"user123","update_data":{"name":"John Doe","mailing_address":"123 Main St"}})
    assert resp.status_code == 200
    assert resp.json() is None

def test_initiate_account_update_missing_fields():
    resp = client.post("/controllers/initiate_account_update", json={"user_id":"user123","update_data":{"mailing_address":"123 Main St"}})
    assert resp.status_code >= 400

def test_update_user_details_anchor():
    resp = client.post("/controllers/update_user_details", json={"user_id":"user123","name":"John Doe","mailing_address":"123 Main St","billing_address":"456 Oak Ave","payment_info":{"card_number":"1234567890123456","expiry_date":"12/25"}})
    assert resp.status_code == 200
    assert resp.json() is True

def test_update_user_details_empty_strings():
    resp = client.post("/controllers/update_user_details", json={"user_id":"user123","name":"","mailing_address":"","billing_address":"456 Oak Ave","payment_info":{"card_number":"1234567890123456","expiry_date":"12/25"}})
    assert resp.status_code == 200
    assert resp.json() is True

def test_change_password_anchor():
    resp = client.post("/controllers/change_password", json={"user_id":"user123","old_password":"oldpass123","new_password":"newpass456","confirm_new_password":"newpass456"})
    assert resp.status_code == 200
    assert resp.json() is True

def test_change_password_mismatched_new_passwords():
    resp = client.post("/controllers/change_password", json={"user_id":"user123","old_password":"oldpass123","new_password":"newpass456","confirm_new_password":"differentpass789"})
    assert resp.status_code >= 400
