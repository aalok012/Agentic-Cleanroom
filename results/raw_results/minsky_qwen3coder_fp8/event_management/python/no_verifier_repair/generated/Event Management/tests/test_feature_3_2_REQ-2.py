"""Spec-derived pytest module for feature 3.2.REQ-2.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_register_for_event():
    # Test case 1: Canonical case
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    assert resp.status_code == 200
    assert resp.json() == True

    # Test case 2: User not authenticated
    resp = client.post("/controllers/register_for_event", json={"user_id":"","event_id":"event_456"})
    assert resp.status_code >= 400

    # Test case 3: User authenticated but not enrolled
    client.post("/controllers/register_for_event", json={"user_id":"user_789", "role": "faculty"})
    resp = client.post("/controllers/register_for_event", json={"user_id":"user_789","event_id":"event_456"})
    assert resp.status_code >= 400

    # Test case 4: Event does not exist
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_999"})
    assert resp.status_code >= 400

    # Test case 5: Student already registered
    client.post("/controllers/register_for_event", json={"user_id":"student_123", "event_id": "event_456"})
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    assert resp.status_code >= 400
