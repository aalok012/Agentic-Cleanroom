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

def test_append_event_missing_description():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Meeting"}})
    assert resp.status_code >= 400

def test_append_event_empty_description():
    resp = client.post("/models/append_event", json={"event_data":{"title":"Meeting","description":""}})
    assert resp.status_code >= 400
