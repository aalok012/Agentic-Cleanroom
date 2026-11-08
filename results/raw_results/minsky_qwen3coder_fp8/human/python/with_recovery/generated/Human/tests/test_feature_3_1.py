"""Spec-derived pytest module for feature 3.1.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.human.python.with_recovery.generated.Human.app import create_app

client = TestClient(create_app())

def test_edit_event_details_and_registration_anchor_case():
    # Setup is not needed for this case
    resp = client.post("/controllers/edit_event_details_and_registration", json={"event_id":"evt-123","details":{"title":"Updated Title","description":"New Description"},"registration_requirements":{"age_limit":18}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_edit_event_details_and_registration_empty_details():
    # Seed the event first
    client.post("/controllers/edit_event_details_and_registration", json={"event_id":"evt-123","details":{"title":"Original Title","description":"Original Description"},"registration_requirements":{"age_limit":18}})
    
    # Now edit with empty details
    resp = client.post("/controllers/edit_event_details_and_registration", json={"event_id":"evt-123","details":{},"registration_requirements":{"age_limit":18}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_edit_event_details_and_registration_missing_registration_requirements():
    # Seed the event first
    client.post("/controllers/edit_event_details_and_registration", json={"event_id":"evt-123","details":{"title":"Original Title","description":"Original Description"},"registration_requirements":{"age_limit":18}})
    
    # Now edit with empty registration requirements
    resp = client.post("/controllers/edit_event_details_and_registration", json={"event_id":"evt-123","details":{"title":"Updated Title","description":"New Description"},"registration_requirements":{}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_edit_event_details_and_registration_not_found():
    # Attempt to edit a non-existent event
    resp = client.post("/controllers/edit_event_details_and_registration", json={"event_id":"evt-nonexistent","details":{"title":"Updated Title","description":"New Description"},"registration_requirements":{"age_limit":18}})
    assert resp.status_code >= 400

def test_edit_event_details_and_registration_invalid_event_id_type():
    # Attempt to edit with invalid event ID type
    resp = client.post("/controllers/edit_event_details_and_registration", json={"event_id":123,"details":{"title":"Updated Title","description":"New Description"},"registration_requirements":{"age_limit":18}})
    assert resp.status_code >= 400
