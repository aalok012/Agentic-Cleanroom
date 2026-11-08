"""Spec-derived pytest module for feature 3.2.REQ-8.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case():
    resp = client.post("/controllers/fr_3_2_REQ_8", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_additional_fields_in_request():
    resp = client.post("/controllers/fr_3_2_REQ_8", json={"request": {"extra_field": "value"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_nested_object_in_request():
    resp = client.post("/controllers/fr_3_2_REQ_8", json={"request": {"nested": {"key": "value"}}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_null_value_in_request():
    resp = client.post("/controllers/fr_3_2_REQ_8", json={"request": {"null_field": None}})
    assert resp.status_code == 200
    assert resp.json() == {}
