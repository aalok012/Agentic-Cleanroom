"""Spec-derived pytest module for feature 3.2.REQ-4.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_post_event_on_website_valid():
    resp = client.post("/models/post_event_on_website", json={"event_data":{"title":"Workshop on AI","description":"A workshop on artificial intelligence","date":"2023-10-15","time":"10:00","location":"Online","registration_details":"Register at the link below"}})
    assert resp.status_code == 200
    assert resp.json() == {"event_id": 123, "status": "published"}

def test_post_event_on_website_missing_fields():
    resp = client.post("/models/post_event_on_website", json={"event_data":{"title":"Workshop on AI","date":"2023-10-15","time":"10:00","location":"Online","registration_details":"Register at the link below"}})
    assert resp.status_code >= 400

def test_post_event_on_website_empty_title():
    resp = client.post("/models/post_event_on_website", json={"event_data":{"title":"","description":"A workshop on artificial intelligence","date":"2023-10-15","time":"10:00","location":"Online","registration_details":"Register at the link below"}})
    assert resp.status_code >= 400

def test_post_event_on_website_invalid_date_format():
    resp = client.post("/models/post_event_on_website", json={"event_data":{"title":"Workshop on AI","description":"A workshop on artificial intelligence","date":"15-10-2023","time":"10:00","location":"Online","registration_details":"Register at the link below"}})
    assert resp.status_code >= 400
