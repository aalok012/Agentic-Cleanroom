"""Spec-derived pytest module for feature 4.14.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_logout_user_canonical():
    resp = client.post("/controllers/logout_user", json={})
    assert resp.status_code == 200
    assert resp.json() == {"message": "User logged out successfully"}

def test_logout_user_extra_fields():
    resp = client.post("/controllers/logout_user", json={"extra_field": "value"})
    assert resp.status_code == 200
    assert resp.json() == {"message": "User logged out successfully"}

def test_logout_user_no_session():
    resp = client.post("/controllers/logout_user", json={})
    assert resp.status_code == 200
    assert resp.json() == {"message": "User logged out successfully"}

def test_logout_user_malformed_input():
    # Sending a string instead of a JSON object
    resp = client.post("/controllers/logout_user", content="invalid_json")
    assert resp.status_code >= 400
