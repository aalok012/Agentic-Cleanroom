"""Spec-derived pytest module for feature 3.2.REQ-11.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case_empty_database():
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == []

def test_independent_single_event():
    client.post("/events/add", json={"action": "add", "event": {"id": "1", "name": "Event A", "timestamp": "2023-01-01T00:00:00Z"}})
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "1", "name": "Event A", "timestamp": "2023-01-01T00:00:00Z"}]

def test_independent_multiple_events_different_order():
    client.post("/events/add", json={"action": "add", "event": {"id": "2", "name": "Event B", "timestamp": "2023-01-02T00:00:00Z"}})
    client.post("/events/add", json={"action": "add", "event": {"id": "1", "name": "Event A", "timestamp": "2023-01-01T00:00:00Z"}})
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "1", "name": "Event A", "timestamp": "2023-01-01T00:00:00Z"}, {"id": "2", "name": "Event B", "timestamp": "2023-01-02T00:00:00Z"}]

def test_independent_duplicate_timestamps():
    client.post("/events/add", json={"action": "add", "event": {"id": "1", "name": "Event A", "timestamp": "2023-01-01T00:00:00Z"}})
    client.post("/events/add", json={"action": "add", "event": {"id": "2", "name": "Event B", "timestamp": "2023-01-01T00:00:00Z"}})
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "1", "name": "Event A", "timestamp": "2023-01-01T00:00:00Z"}, {"id": "2", "name": "Event B", "timestamp": "2023-01-01T00:00:00Z"}]
