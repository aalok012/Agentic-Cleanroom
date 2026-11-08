"""Spec-derived pytest module for feature 3.2.REQ-3.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_display_error_message_success():
    # Test case 1: Canonical success case
    resp = client.post("/views/display_error_message", json={"error_type":"validation","user_action":"submitting an empty form"})
    assert resp.status_code == 200
    assert resp.json() == "Please fill in all required fields."

def test_display_error_message_default():
    # Test case 2: Default error message when no match found
    resp = client.post("/views/display_error_message", json={"error_type":"unknown_error","user_action":"performing an invalid action"})
    assert resp.status_code == 200
    assert resp.json() == "An unexpected error occurred. Please try again later."

def test_display_error_message_missing_error_type():
    # Test case 3: Missing error_type should raise HTTPException
    resp = client.post("/views/display_error_message", json={"user_action":"submitting an empty form"})
    assert resp.status_code >= 400

def test_display_error_message_missing_user_action():
    # Test case 4: Missing user_action should raise HTTPException
    resp = client.post("/views/display_error_message", json={"error_type":"validation"})
    assert resp.status_code >= 400

def test_display_error_message_with_db_entry():
    # Test case 5: Using database entry for authentication error
    # First, add the error message to the database
    client.post("/views/display_error_message", json={"error_type": "authentication", "user_action": "logging in", "message": "Invalid username or password. Please try again."})
    
    # Now test that the correct message is returned
    resp = client.post("/views/display_error_message", json={"error_type":"authentication","user_action":"logging in"})
    assert resp.status_code == 200
    assert resp.json() == "Invalid username or password. Please try again."
