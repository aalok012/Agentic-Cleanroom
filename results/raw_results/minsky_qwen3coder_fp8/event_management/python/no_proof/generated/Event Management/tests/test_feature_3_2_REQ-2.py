"""Spec-derived pytest module for feature 3.2.REQ-2.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_register_for_event_anchor_case():
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_register_for_event_empty_user_id():
    resp = client.post("/controllers/register_for_event", json={"user_id":"","event_id":"event_456"})
    assert resp.status_code >= 400

def test_register_for_event_non_enrolled_user():
    # Arrange
    client.post("/controllers/add_user", json={"action": "add", "user": {"id": "user_789", "name": "John Doe", "is_enrolled": False}})
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"user_789","event_id":"event_456"})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == False

def test_register_for_event_user_not_found():
    resp = client.post("/controllers/register_for_event", json={"user_id":"nonexistent_user","event_id":"event_456"})
    assert resp.status_code >= 400

def test_register_for_event_event_not_found():
    # Arrange
    client.post("/controllers/add_event", json={"action": "add", "event": {"id": "event_999", "name": "Non-existent Event"}})
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_999"})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == False
