"""Spec-derived pytest module for feature 3.2.REQ-10.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_append_event_valid():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Meeting","description":"Team meeting"}})
    assert resp.status_code == 200
    assert resp.json() is None

def test_append_event_missing_title():
    resp = client.post("/models/append_event", json={"event_data":{"description":"Team meeting"}})
    assert resp.status_code >= 400

def test_append_event_empty_title():
    resp = client.post("/models/append_event", json={"event_data":{"title":"","description":"Team meeting"}})
    assert resp.status_code >= 400

def test_append_event_special_characters():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Meeting & Conference","description":"Team meeting"}})
    assert resp.status_code == 200
    assert resp.json() is None

def test_append_event_long_description():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Meeting","description":"This is a very long description that exceeds typical length limits and tests the database's ability to handle large text inputs without errors."}})
    assert resp.status_code == 200
    assert resp.json() is None
