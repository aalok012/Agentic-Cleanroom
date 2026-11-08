"""Spec-derived pytest module for feature 3.2.REQ-3.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_display_error_message_canonical():
    resp = client.post("/views/display_error_message", json={"error_type":"validation","user_action":"submitting an empty form"})
    assert resp.status_code == 200
    assert resp.json() == "Please fill in all required fields."

def test_display_error_message_invalid_error_type():
    resp = client.post("/views/display_error_message", json={"error_type":"invalid_type","user_action":"submitting a form"})
    assert resp.status_code >= 400

def test_display_error_message_empty_user_action():
    resp = client.post("/views/display_error_message", json={"error_type":"validation","user_action":""})
    assert resp.status_code == 200
    assert resp.json() == "Please fill in all required fields."

def test_display_error_message_authentication_error():
    resp = client.post("/views/display_error_message", json={"error_type":"authentication","user_action":"accessing restricted content"})
    assert resp.status_code == 200
    assert resp.json() == "You must be logged in to perform this action."

def test_display_error_message_missing_field():
    resp = client.post("/views/display_error_message", json={"user_action":"submitting a form"})
    assert resp.status_code >= 400
