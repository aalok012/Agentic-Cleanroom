"""Spec-derived pytest module for feature 3.2.REQ-3.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_fr_3_2_REQ_3_anchor_case():
    resp = client.post("/controllers/fr_3_2_REQ_3", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_3_2_REQ_3_invalid_key_type():
    resp = client.post("/controllers/fr_3_2_REQ_3", json={"request": {"123": "value"}})
    assert resp.status_code >= 400

def test_fr_3_2_REQ_3_malformed_json():
    # This would be handled by FastAPI's automatic validation
    # We simulate by sending invalid JSON which should fail during parsing
    resp = client.post("/controllers/fr_3_2_REQ_3", content="{"""request":{", headers={"Content-Type": "application/json"})
    assert resp.status_code >= 400

def test_fr_3_2_REQ_3_unexpected_nested_structure():
    resp = client.post("/controllers/fr_3_2_REQ_3", json={"request": {"nested": {"key": "value"}}})
    assert resp.status_code >= 400
