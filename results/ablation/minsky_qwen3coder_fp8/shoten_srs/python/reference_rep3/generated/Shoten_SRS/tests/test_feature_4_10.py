"""Spec-derived pytest module for feature 4.10.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_get_seller_contact_methods_anchor():
    resp = client.post("/views/get_seller_contact_methods", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"type": "bookstore", "contact": "phone: 123-456-7890"}, {"type": "printstore", "contact": "email: print@example.com"}]

def test_get_seller_contact_methods_empty():
    resp = client.post("/views/get_seller_contact_methods", json={})
    assert resp.status_code == 200
    assert resp.json() == []

def test_get_seller_details_anchor():
    resp = client.post("/views/get_seller_details", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"type": "bookstore", "address": "123 Main St", "phone": "123-456-7890", "email": "info@bookstore.com", "directions": "Take Highway 101 North"}]

def test_get_seller_details_missing_fields():
    resp = client.post("/views/get_seller_details", json={})
    assert resp.status_code == 200
    assert resp.json() == [{"type": "bookstore", "address": "123 Main St", "phone": "123-456-7890", "email": "info@bookstore.com", "directions": "Take Highway 101 North"}]

def test_get_seller_locations_map_anchor():
    resp = client.post("/views/get_seller_locations_map", json={})
    assert resp.status_code == 200
    assert resp.json() == "https://maps.example.com/bookstore-printstore-map"

def test_get_seller_locations_map_invalid_url():
    resp = client.post("/views/get_seller_locations_map", json={})
    assert resp.status_code == 200
    assert resp.json() == "https://maps.example.com/bookstore-printstore-map"
