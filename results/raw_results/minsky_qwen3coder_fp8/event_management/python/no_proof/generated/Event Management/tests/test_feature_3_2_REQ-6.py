"""Spec-derived pytest module for feature 3.2.REQ-6.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case():
    resp = client.post("/models/stakeholder_database", json={})
    assert resp.status_code == 200
    assert resp.json() is None

def test_unexpected_field():
    resp = client.post("/models/stakeholder_database", json={"unexpected_field": "value"})
    assert resp.status_code >= 400

def test_incorrect_field_type():
    resp = client.post("/models/stakeholder_database", json={"credentials": "invalid_type"})
    assert resp.status_code >= 400

def test_missing_required_field():
    resp = client.post("/models/stakeholder_database", json={"login_credentials": {"username": "user1", "password": "pass1"}})
    assert resp.status_code >= 400
