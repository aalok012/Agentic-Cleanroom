"""Spec-derived pytest module for feature 3.2.REQ-2.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_canonical_success():
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_non_enrolled_user():
    resp = client.post("/controllers/register_for_event", json={"user_id":"unenrolled_user","event_id":"event_456"})
    assert resp.status_code >= 400

def test_missing_user_id():
    resp = client.post("/controllers/register_for_event", json={"user_id":"","event_id":"event_456"})
    assert resp.status_code >= 400

def test_missing_event_id():
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":""})
    assert resp.status_code >= 400

def test_non_authenticated_user():
    resp = client.post("/controllers/register_for_event", json={"user_id":"non_auth_user","event_id":"event_456"})
    assert resp.status_code >= 400
