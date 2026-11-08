"""Spec-derived pytest module for feature 3.2.REQ-4.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_post_event_on_website_valid():
    resp = client.post("/controllers/post_event_on_website", json={"event_data":{"title":"Tech Conference","description":"Annual tech conference","date":"2023-10-15","time":"10:00","registration_deadline":"2023-10-10"}})
    assert resp.status_code == 200
    assert resp.json() == {"event_id": "evt_12345", "status": "published"}

def test_post_event_on_website_missing_title():
    resp = client.post("/controllers/post_event_on_website", json={"event_data":{"description":"Annual tech conference","date":"2023-10-15","time":"10:00","registration_deadline":"2023-10-10"}})
    assert resp.status_code >= 400

def test_post_event_on_website_empty_title():
    resp = client.post("/controllers/post_event_on_website", json={"event_data":{"title":"","description":"Annual tech conference","date":"2023-10-15","time":"10:00","registration_deadline":"2023-10-10"}})
    assert resp.status_code >= 400

def test_post_event_on_website_invalid_date_format():
    resp = client.post("/controllers/post_event_on_website", json={"event_data":{"title":"Tech Conference","description":"Annual tech conference","date":"15-10-2023","time":"10:00","registration_deadline":"2023-10-10"}})
    assert resp.status_code >= 400

def test_post_event_on_website_invalid_time_format():
    resp = client.post("/controllers/post_event_on_website", json={"event_data":{"title":"Tech Conference","description":"Annual tech conference","date":"2023-10-15","time":"10.00","registration_deadline":"2023-10-10"}})
    assert resp.status_code >= 400
