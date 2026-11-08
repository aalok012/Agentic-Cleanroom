"""Spec-derived pytest module for feature 4.7.

Generated black-box from the specification (10 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_req_1_anchor():
    resp = client.post("/controllers/process_purchase", json={"user_id":"user123","cart_items":[{"title":"Book A","price":10.99,"quantity":2},{"title":"Book B","price":5.5,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "purchased_items": [{"title": "Book A", "price": 10.99, "quantity": 2}, {"title": "Book B", "price": 5.50, "quantity": 1}], "total_cost": 27.48}

def test_req_1_failure():
    resp = client.post("/controllers/process_purchase", json={"user_id":"","cart_items":[{"title":"Book A","price":10.99,"quantity":2}]})
    assert resp.status_code >= 400

def test_req_2_anchor():
    resp = client.post("/models/calculate_cart_total", json={"cart_items":[{"price":10.99,"quantity":2},{"price":5.5,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == 27.48

def test_req_2_failure():
    resp = client.post("/models/calculate_cart_total", json={"cart_items":[]})
    assert resp.status_code >= 400

def test_req_3_anchor():
    resp = client.post("/controllers/save_delivery_info", json={"user_id":"user123","delivery_info":{"street":"123 Main St","city":"Anytown","zip_code":"12345"}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_req_3_failure():
    resp = client.post("/controllers/save_delivery_info", json={"user_id":"user123","delivery_info":{}})
    assert resp.status_code >= 400

def test_req_4_anchor():
    resp = client.post("/views/prompt_payment_info", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Please enter your payment information"}

def test_req_4_failure():
    resp = client.post("/views/prompt_payment_info", json={"user_id":""})
    assert resp.status_code >= 400

def test_req_5_anchor():
    resp = client.post("/views/display_purchased_books", json={"purchase_details":{"purchased_items":[{"title":"Book A","price":10.99,"quantity":2},{"title":"Book B","price":5.5,"quantity":1}]}})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Book A", "price": 10.99, "quantity": 2}, {"title": "Book B", "price": 5.50, "quantity": 1}]

def test_req_5_failure():
    resp = client.post("/views/display_purchased_books", json={"purchase_details":{}})
    assert resp.status_code >= 400
