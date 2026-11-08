"""Spec-derived pytest module for feature 4.6.

Generated black-box from the specification (12 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_req_1_anchor():
    resp = client.post("/controllers/initiate_rental_process", json={"user_id":"user123","cart_items":[{"title":"Book A","price":10.99},{"title":"Book B","price":15.5}]})
    assert resp.status_code == 200
    assert resp.json() == True

def test_req_1_failure():
    resp = client.post("/controllers/initiate_rental_process", json={"user_id":"","cart_items":[]})
    assert resp.status_code >= 400

def test_req_2_anchor():
    resp = client.post("/views/prompt_rental_period_input", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"prompt": "Please enter the rental period", "form_fields": ["duration"]}

def test_req_2_failure():
    resp = client.post("/views/prompt_rental_period_input", json={"user_id":""})
    assert resp.status_code >= 400

def test_req_3_anchor():
    resp = client.post("/controllers/calculate_and_display_rent", json={"cart_items":[{"title":"Book A","price":10.99,"quantity":2},{"title":"Book B","price":15.5,"quantity":1}],"rental_duration":"1 week"})
    assert resp.status_code == 200
    assert resp.json() == {"total_rent": 37.48, "individual_rents": [{"title": "Book A", "rent": 21.98}, {"title": "Book B", "rent": 15.5}]}

def test_req_3_failure():
    resp = client.post("/controllers/calculate_and_display_rent", json={"cart_items":[],"rental_duration":"invalid"})
    assert resp.status_code >= 400

def test_req_4_anchor():
    resp = client.post("/controllers/collect_delivery_information", json={"user_id":"user123","delivery_details":{"address":"123 Main St","contact":"555-1234"}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_req_4_failure():
    resp = client.post("/controllers/collect_delivery_information", json={"user_id":"","delivery_details":{}})
    assert resp.status_code >= 400

def test_req_5_anchor():
    resp = client.post("/views/prompt_payment_information", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"prompt": "Please enter your payment information", "form_fields": ["card_number", "expiry_date", "cvv"]}

def test_req_5_failure():
    resp = client.post("/views/prompt_payment_information", json={"user_id":""})
    assert resp.status_code >= 400

def test_req_6_anchor():
    resp = client.post("/views/display_rented_books", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Book A", "price": 10.99, "quantity": 2}, {"title": "Book B", "price": 15.5, "quantity": 1}]

def test_req_6_failure():
    resp = client.post("/views/display_rented_books", json={"user_id":""})
    assert resp.status_code >= 400
