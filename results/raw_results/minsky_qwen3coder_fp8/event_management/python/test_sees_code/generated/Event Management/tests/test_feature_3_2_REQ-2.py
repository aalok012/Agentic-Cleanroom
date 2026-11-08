"""Spec-derived pytest module for feature 3.2.REQ-2.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

class User:
    def __init__(self, id, is_enrolled):
        self.id = id
        self.is_enrolled = is_enrolled

class Event:
    def __init__(self, id):
        self.id = id

class Registration:
    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

client = TestClient(create_app())

def test_register_for_event_canonical_case():
    # Arrange
    user_data = {"id": "student_123", "is_enrolled": True}
    event_data = {"id": "event_456"}
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == True

def test_register_for_event_empty_user_id():
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"","event_id":"event_456"})
    
    # Assert
    assert resp.status_code >= 400

def test_register_for_event_unenrolled_user():
    # Arrange
    user_data = {"id": "user_not_enrolled", "is_enrolled": False}
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"user_not_enrolled","event_id":"event_456"})
    
    # Assert
    assert resp.status_code >= 400

def test_register_for_event_nonexistent_event():
    # Arrange
    user_data = {"id": "student_123", "is_enrolled": True}
    
    # Act
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"nonexistent_event"})
    
    # Assert
    assert resp.status_code >= 400

def test_register_for_event_already_registered():
    # Arrange
    user_data = {"id": "student_123", "is_enrolled": True}
    event_data = {"id": "event_456"}
    
    # First registration
    client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    
    # Second registration attempt
    resp = client.post("/controllers/register_for_event", json={"user_id":"student_123","event_id":"event_456"})
    
    # Assert
    assert resp.status_code == 200
    assert resp.json() == True
