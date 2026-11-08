"""Spec-derived pytest module for feature 4.6.

Generated black-box from the specification (12 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_rent_feature():
    # Test REQ-1
    resp = client.post("/controllers/initiate_rental_process", json={"user_id":"user123","shopping_cart":[{"title":"Book A","price":10.99,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == True

    resp = client.post("/controllers/initiate_rental_process", json={"user_id":"","shopping_cart":[{"title":"Book A","price":10.99,"quantity":1}]})
    assert resp.status_code >= 400

    # Test REQ-2
    resp = client.post("/views/prompt_rental_period", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"form": "rental_duration_form", "fields": ["duration"]}

    resp = client.post("/views/prompt_rental_period", json={"user_id":""})
    assert resp.status_code >= 400

    # Test REQ-3
    resp = client.post("/controllers/calculate_and_display_rent", json={"user_id":"user123","rental_period":"1 week"})
    assert resp.status_code == 200
    assert resp.json() == {"total_rent": 21.98, "individual_rents": [{"title": "Book A", "rent": 10.99}, {"title": "Book B", "rent": 10.99}]}

    resp = client.post("/controllers/calculate_and_display_rent", json={"user_id":"user123","rental_period":"invalid_period"})
    assert resp.status_code >= 400

    # Test REQ-4
    resp = client.post("/controllers/collect_delivery_information", json={"user_id":"user123","delivery_details":{"address":"123 Main St","contact":"555-1234"}})
    assert resp.status_code == 200
    assert resp.json() == True

    resp = client.post("/controllers/collect_delivery_information", json={"user_id":"user123","delivery_details":{}})
    assert resp.status_code >= 400

    # Test REQ-5
    resp = client.post("/views/prompt_payment_information", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"form": "payment_form", "fields": ["card_number", "expiry_date", "cvv"]}

    resp = client.post("/views/prompt_payment_information", json={"user_id":""})
    assert resp.status_code >= 400

    # Test REQ-6
    resp = client.post("/views/display_rented_books", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Book A", "price": 10.99, "quantity": 1}, {"title": "Book B", "price": 10.99, "quantity": 1}]

    resp = client.post("/views/display_rented_books", json={"user_id":""})
    assert resp.status_code >= 400
