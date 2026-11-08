"""Spec-derived pytest module for feature 4.7.

Generated black-box from the specification (9 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_requirement_4_7_REQ_1_anchor():
    resp = client.post("/controllers/process_purchase", json={"user_id":"user123","cart_items":[{"title":"Book A","price":10.99,"quantity":2},{"title":"Book B","price":5.5,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "purchased_items": [{"title": "Book A", "price": 10.99, "quantity": 2}, {"title": "Book B", "price": 5.50, "quantity": 1}], "total_cost": 27.48}

def test_requirement_4_7_REQ_1_failure():
    resp = client.post("/controllers/process_purchase", json={"user_id":"","cart_items":[{"title":"Book A","price":10.99,"quantity":2}]})
    assert resp.status_code >= 400

def test_requirement_4_7_REQ_2_anchor():
    resp = client.post("/models/calculate_shopping_cart_total", json={"cart_items":[{"price":10.99,"quantity":2},{"price":5.5,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == 27.48

def test_requirement_4_7_REQ_2_edge_case_empty_cart():
    resp = client.post("/models/calculate_shopping_cart_total", json={"cart_items":[]})
    assert resp.status_code >= 400

def test_requirement_4_7_REQ_3_anchor():
    resp = client.post("/models/save_delivery_information", json={"user_id":"user123","delivery_info":{"street":"123 Main St","city":"Anytown","zip_code":"12345"}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_requirement_4_7_REQ_3_failure():
    resp = client.post("/models/save_delivery_information", json={"user_id":"","delivery_info":{"street":"123 Main St","city":"Anytown","zip_code":"12345"}})
    assert resp.status_code >= 400

def test_requirement_4_7_REQ_4_anchor():
    resp = client.post("/views/prompt_payment_information_4_7_REQ_4", json={})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Please enter your payment information"}

def test_requirement_4_7_REQ_5_anchor():
    resp = client.post("/views/display_purchased_books", json={"purchased_items":[{"title":"Book A","price":10.99,"quantity":2},{"title":"Book B","price":5.5,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Book A", "price": 10.99, "quantity": 2}, {"title": "Book B", "price": 5.50, "quantity": 1}]

def test_requirement_4_7_REQ_5_edge_case_empty_list():
    resp = client.post("/views/display_purchased_books", json={"purchased_items":[]})
    assert resp.status_code >= 400
