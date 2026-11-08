"""Spec-derived pytest module for feature 4.2.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_req_1_anchor_case():
    resp = client.post("/controllers/login_user", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_req_1_failure_case():
    resp = client.post("/controllers/login_user", json={"username":"johndoe","password":"wrongpass"})
    assert resp.status_code >= 400

def test_req_2_anchor_case():
    resp = client.post("/controllers/validate_login_credentials", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() is None

def test_req_2_missing_username():
    resp = client.post("/controllers/validate_login_credentials", json={"username":"","password":"secret123"})
    assert resp.status_code >= 400

def test_req_2_missing_password():
    resp = client.post("/controllers/validate_login_credentials", json={"username":"johndoe","password":""})
    assert resp.status_code >= 400

def test_req_3_anchor_case():
    resp = client.post("/models/verify_credentials", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_req_3_invalid_password():
    resp = client.post("/models/verify_credentials", json={"username":"johndoe","password":"wrongpass"})
    assert resp.status_code >= 400
