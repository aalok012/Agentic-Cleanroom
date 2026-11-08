"""Spec-derived pytest module for feature 3.2.REQ-2.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_register_for_event_success():
    # Arrange
    # No setup needed for this case
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == {"status": "registered", "user_id": "student_123", "event_id": "event_456"}

def test_register_for_event_missing_user_id():
    # Arrange
    # No setup needed for this case
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"","event_id":"event_456"})
    
    # Assert
    assert resp.status_code >= 400

def test_register_for_event_unenrolled_user():
    # Arrange
    client.post("/controllers/add_user", json={"user_id": "unenrolled_user", "role": "guest"})
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"unenrolled_user","event_id":"event_456"})
    
    # Assert
    assert resp.status_code >= 400

def test_register_for_event_nonexistent_event():
    # Arrange
    # No setup needed for this case
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"nonexistent_event"})
    
    # Assert
    assert resp.status_code >= 400
