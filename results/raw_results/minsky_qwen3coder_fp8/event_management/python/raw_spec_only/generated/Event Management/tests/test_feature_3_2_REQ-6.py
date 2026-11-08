"""Spec-derived pytest module for feature 3.2.REQ-6.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_canonical_case():
    resp = client.post("/controllers/fr_3_2_REQ_6", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_request_with_additional_fields():
    resp = client.post("/controllers/fr_3_2_REQ_6", json={"request": {"extra_field": "value"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_request_with_nested_object():
    resp = client.post("/controllers/fr_3_2_REQ_6", json={"request": {"nested": {"key": "value"}}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_malformed_request_body():
    resp = client.post("/controllers/fr_3_2_REQ_6", json={"request": []})
    assert resp.status_code >= 400
