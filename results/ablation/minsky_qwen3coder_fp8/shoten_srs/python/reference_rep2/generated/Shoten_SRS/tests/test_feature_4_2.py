"""Spec-derived pytest module for feature 4.2.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_requirement_4_2_REQ_1():
    # Anchor case
    resp = client.post("/controllers/login_user", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == True

    # Independent case
    resp = client.post("/controllers/login_user", json={"username":"johndoe","password":"wrongpass"})
    assert resp.status_code >= 400

def test_requirement_4_2_REQ_2():
    # Anchor case
    resp = client.post("/controllers/validate_login_credentials", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == True

    # Independent case
    resp = client.post("/controllers/validate_login_credentials", json={"username":"","password":"secret123"})
    assert resp.status_code >= 400

def test_requirement_4_2_REQ_3():
    # Anchor case
    resp = client.post("/models/authenticate_user", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == {"session_token": "abc123xyz", "user_id": "user123"}

    # Independent case
    resp = client.post("/models/authenticate_user", json={"username":"johndoe","password":"wrongpass"})
    assert resp.status_code >= 400
