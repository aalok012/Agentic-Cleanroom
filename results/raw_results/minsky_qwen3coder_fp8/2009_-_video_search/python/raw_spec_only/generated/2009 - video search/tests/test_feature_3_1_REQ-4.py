"""Spec-derived pytest module for feature 3.1.REQ-4.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case():
    resp = client.post("/controllers/fr_3_1_REQ_4", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_empty_request_body():
    resp = client.post("/controllers/fr_3_1_REQ_4", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_additional_fields_in_request():
    resp = client.post("/controllers/fr_3_1_REQ_4", json={"request": {"extra_field": "value"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_malformed_request_structure():
    resp = client.post("/controllers/fr_3_1_REQ_4", json={"request": "invalid_structure"})
    assert resp.status_code >= 400
