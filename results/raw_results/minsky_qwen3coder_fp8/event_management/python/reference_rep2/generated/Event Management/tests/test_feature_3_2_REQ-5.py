"""Spec-derived pytest module for feature 3.2.REQ-5.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case():
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "John Doe", "email": "john@example.com"}, {"name": "Jane Smith", "email": "jane@example.com"}]

def test_empty_registrant_list():
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == []

def test_single_registrant():
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Alice Johnson", "email": "alice@example.com"}})
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "Alice Johnson", "email": "alice@example.com"}]

def test_multiple_registrants():
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Bob Smith", "email": "bob@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Charlie Brown", "email": "charlie@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Diana Prince", "email": "diana@example.com"}})
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "Bob Smith", "email": "bob@example.com"}, {"name": "Charlie Brown", "email": "charlie@example.com"}, {"name": "Diana Prince", "email": "diana@example.com"}]
