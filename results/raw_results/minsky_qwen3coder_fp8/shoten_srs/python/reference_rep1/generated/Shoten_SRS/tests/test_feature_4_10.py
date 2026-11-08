"""Spec-derived pytest module for feature 4.10.

Generated black-box from the specification (3 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_get_seller_contact_methods_anchor():
    resp = client.post("/views/get_seller_contact_methods", json={})
    assert resp.status_code == 200
    assert resp.json() == {
        "bookstore": ["email: bookstore@example.com", "phone: 123-456-7890"],
        "printstore": ["email: printstore@example.com", "phone: 098-765-4321"],
        "student": ["email: student@example.com", "phone: 555-555-5555"]
    }

def test_get_seller_details_anchor():
    resp = client.post("/views/get_seller_details", json={})
    assert resp.status_code == 200
    assert resp.json() == {
        "bookstore": {
            "address": "123 Main St",
            "phone": "123-456-7890",
            "email": "bookstore@example.com",
            "directions": "Take the first left after the library"
        },
        "printstore": {
            "address": "456 Oak Ave",
            "phone": "098-765-4321",
            "email": "printstore@example.com",
            "directions": "Turn right at the gas station"
        }
    }

def test_get_seller_locations_map_anchor():
    resp = client.post("/views/get_seller_locations_map", json={})
    assert resp.status_code == 200
    assert resp.json() == "https://maps.example.com/sellers"
