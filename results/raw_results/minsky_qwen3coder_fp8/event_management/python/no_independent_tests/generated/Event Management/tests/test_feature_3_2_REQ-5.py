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
    assert resp.json() == [{"name": "John Doe", "email": "john.doe@example.com"}, {"name": "Jane Smith", "email": "jane.smith@example.com"}]

def test_empty_list_case():
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == []

def test_single_registrant_case():
    # Setup
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Alice Johnson", "email": "alice.johnson@example.com"}})
    
    # Main test
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "Alice Johnson", "email": "alice.johnson@example.com"}]

def test_multiple_registrants_case():
    # Setup
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Bob Smith", "email": "bob.smith@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Charlie Brown", "email": "charlie.brown@example.com"}})
    client.post("/models/add_registrant", json={"action": "add", "registrant": {"name": "Diana Prince", "email": "diana.prince@example.com"}})
    
    # Main test
    resp = client.post("/models/generate_registrant_list", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "Bob Smith", "email": "bob.smith@example.com"}, {"name": "Charlie Brown", "email": "charlie.brown@example.com"}, {"name": "Diana Prince", "email": "diana.prince@example.com"}]
