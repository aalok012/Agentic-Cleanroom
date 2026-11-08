"""Spec-derived pytest module for feature 3.1.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.human.python.no_proof.generated.Human.app import create_app

client = TestClient(create_app())

def test_edit_event_details_and_registration_anchor_case():
    # Setup
    setup_data = {
        "event_id": "evt-123",
        "details": {
            "title": "Original Title",
            "description": "Original Description"
        },
        "registration_requirements": {
            "age_limit": 18
        }
    }
    client.post("/controllers/edit_event_details_and_registration", json=setup_data)
    
    # Main test case
    inputs = {
        "event_id": "evt-123",
        "details": {
            "title": "Updated Title",
            "description": "New Description"
        },
        "registration_requirements": {
            "age_limit": 18
        }
    }
    response = client.post("/controllers/edit_event_details_and_registration", json=inputs)
    assert response.status_code == 200
    assert response.json() == True

def test_edit_event_details_and_registration_empty_details():
    # Setup
    setup_data = {
        "event_id": "evt-123",
        "details": {
            "title": "Original Title",
            "description": "Original Description"
        },
        "registration_requirements": {
            "age_limit": 18
        }
    }
    client.post("/controllers/edit_event_details_and_registration", json=setup_data)
    
    # Main test case
    inputs = {
        "event_id": "evt-123",
        "details": {},
        "registration_requirements": {
            "age_limit": 18
        }
    }
    response = client.post("/controllers/edit_event_details_and_registration", json=inputs)
    assert response.status_code == 200
    assert response.json() == True

def test_edit_event_details_and_registration_missing_registration_requirements():
    # Setup
    setup_data = {
        "event_id": "evt-123",
        "details": {
            "title": "Original Title",
            "description": "Original Description"
        },
        "registration_requirements": {
            "age_limit": 18
        }
    }
    client.post("/controllers/edit_event_details_and_registration", json=setup_data)
    
    # Main test case
    inputs = {
        "event_id": "evt-123",
        "details": {
            "title": "Updated Title",
            "description": "New Description"
        },
        "registration_requirements": {}
    }
    response = client.post("/controllers/edit_event_details_and_registration", json=inputs)
    assert response.status_code == 200
    assert response.json() == True

def test_edit_event_details_and_registration_not_found():
    # Main test case
    inputs = {
        "event_id": "evt-nonexistent",
        "details": {
            "title": "Updated Title",
            "description": "New Description"
        },
        "registration_requirements": {
            "age_limit": 18
        }
    }
    response = client.post("/controllers/edit_event_details_and_registration", json=inputs)
    assert response.status_code >= 400

def test_edit_event_details_and_registration_invalid_event_id_type():
    # Main test case
    inputs = {
        "event_id": 123,
        "details": {
            "title": "Updated Title",
            "description": "New Description"
        },
        "registration_requirements": {
            "age_limit": 18
        }
    }
    response = client.post("/controllers/edit_event_details_and_registration", json=inputs)
    assert response.status_code >= 400
