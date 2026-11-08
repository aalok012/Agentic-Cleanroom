"""Spec-derived pytest module for feature 3.2.REQ-11.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case():
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == []

def test_single_event():
    client.post("/views/add_event", json={"action": "add_event", "event": {"id": "event1", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 1"}})
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "event1", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 1"}]

def test_multiple_events():
    client.post("/views/add_event", json={"action": "add_event", "event": {"id": "event2", "timestamp": "2023-01-02T00:00:00Z", "description": "Event 2"}})
    client.post("/views/add_event", json={"action": "add_event", "event": {"id": "event1", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 1"}})
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "event1", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 1"}, {"id": "event2", "timestamp": "2023-01-02T00:00:00Z", "description": "Event 2"}]

def test_same_timestamps():
    client.post("/views/add_event", json={"action": "add_event", "event": {"id": "event2", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 2"}})
    client.post("/views/add_event", json={"action": "add_event", "event": {"id": "event1", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 1"}})
    resp = client.post("/views/get_ordered_events", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "event1", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 1"}, {"id": "event2", "timestamp": "2023-01-01T00:00:00Z", "description": "Event 2"}]
