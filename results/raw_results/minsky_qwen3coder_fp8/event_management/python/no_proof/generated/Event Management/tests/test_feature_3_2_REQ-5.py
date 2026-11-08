"""Spec-derived pytest module for feature 3.2.REQ-5.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_generate_registrant_list_anchor_case():
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "John Doe", "email": "john.doe@example.com"}, {"name": "Jane Smith", "email": "jane.smith@example.com"}]

def test_generate_registrant_list_empty_list():
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == []

def test_generate_registrant_list_single_registrant():
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Alice Johnson", "email": "alice.johnson@example.com"}})
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "Alice Johnson", "email": "alice.johnson@example.com"}]

def test_generate_registrant_list_large_list():
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "John Doe", "email": "john.doe@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Jane Smith", "email": "jane.smith@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Bob Brown", "email": "bob.brown@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Charlie Davis", "email": "charlie.davis@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Diana Evans", "email": "diana.evans@example.com"}})
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "John Doe", "email": "john.doe@example.com"}, {"name": "Jane Smith", "email": "jane.smith@example.com"}, {"name": "Bob Brown", "email": "bob.brown@example.com"}, {"name": "Charlie Davis", "email": "charlie.davis@example.com"}, {"name": "Diana Evans", "email": "diana.evans@example.com"}]
