"""Spec-derived pytest module for feature 3.2.REQ-10.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_append_event_valid():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Team Meeting","description":"Weekly team sync","date":"2023-05-15"}})
    assert resp.status_code == 200
    assert resp.json() is None

def test_append_event_missing_fields():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Team Meeting","date":"2023-05-15"}})
    assert resp.status_code >= 400

def test_append_event_empty_title():
    resp = client.post("/models/append_event", json={"event_data":{"title":"","description":"Weekly team sync","date":"2023-05-15"}})
    assert resp.status_code >= 400

def test_append_event_malformed_date():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Team Meeting","description":"Weekly team sync","date":"invalid-date"}})
    assert resp.status_code >= 400
