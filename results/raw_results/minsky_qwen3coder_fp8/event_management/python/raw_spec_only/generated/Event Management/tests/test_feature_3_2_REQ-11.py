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
    resp = client.post("/controllers/fr_3_2_REQ_11", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_with_event_data():
    resp = client.post("/controllers/fr_3_2_REQ_11", json={"request": {"events": [{"id": 1, "name": "Event A"}, {"id": 2, "name": "Event B"}]}})
    assert resp.status_code == 200
    assert resp.json() == {"events": [{"id": 1, "name": "Event A"}, {"id": 2, "name": "Event B"}]}

def test_malformed_event_data():
    resp = client.post("/controllers/fr_3_2_REQ_11", json={"request": {"events": [{"invalid_field": "value"}]}})
    assert resp.status_code >= 400

def test_missing_events_key():
    resp = client.post("/controllers/fr_3_2_REQ_11", json={"request": {"other_data": "value"}})
    assert resp.status_code >= 400
