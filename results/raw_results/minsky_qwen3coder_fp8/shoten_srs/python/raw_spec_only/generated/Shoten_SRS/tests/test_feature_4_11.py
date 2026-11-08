"""Spec-derived pytest module for feature 4.11.

Generated black-box from the specification (9 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_fr_4_11_REQ_1_anchor():
    resp = client.post("/controllers/fr_4_11_REQ_1", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_4_11_REQ_1_valid_fields():
    resp = client.post("/controllers/fr_4_11_REQ_1", json={"request": {"name": "John Doe", "mailing_address": "123 Main St", "billing_address": "456 Oak Ave", "payment_info": "Visa ending in 1234"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_4_11_REQ_1_invalid_field_type():
    resp = client.post("/controllers/fr_4_11_REQ_1", json={"request": {"name": 123}})
    assert resp.status_code >= 400

def test_fr_4_11_REQ_2_anchor():
    resp = client.post("/controllers/fr_4_11_REQ_2", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_4_11_REQ_2_all_fields_updated():
    resp = client.post("/controllers/fr_4_11_REQ_2", json={"request": {"name": "Jane Smith", "mailing_address": "789 Pine Rd", "billing_address": "321 Elm St", "payment_info": "Mastercard ending in 5678"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_4_11_REQ_2_missing_fields():
    resp = client.post("/controllers/fr_4_11_REQ_2", json={"request": {"name": "Bob Johnson", "mailing_address": "555 Maple Ln"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_4_11_REQ_3_anchor():
    resp = client.post("/controllers/fr_4_11_REQ_3", json={"request": {"old_password": "oldpass123", "new_password": "newpass456", "confirm_new_password": "newpass456"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_4_11_REQ_3_mismatched_passwords():
    resp = client.post("/controllers/fr_4_11_REQ_3", json={"request": {"old_password": "oldpass123", "new_password": "newpass456", "confirm_new_password": "differentpass789"}})
    assert resp.status_code >= 400

def test_fr_4_11_REQ_3_incorrect_old_password():
    resp = client.post("/controllers/fr_4_11_REQ_3", json={"request": {"old_password": "wrongpass123", "new_password": "newpass456", "confirm_new_password": "newpass456"}})
    assert resp.status_code >= 400
