"""Spec-derived pytest module for feature 4.13.

Generated black-box from the specification (11 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_get_user_purchase_history_anchor():
    resp = client.post("/models/get_user_purchase_history", json={"user_id":"user123","days_back":730})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "purchase1", "date": "2023-01-15", "payment_mode": "credit_card", "items": [{"title": "Book Title", "price": 19.99, "quantity": 2}]}]

def test_get_user_purchase_history_boundary():
    # Setup
    client.post("/models/add_purchase", json={"user_id": "user123", "purchase": {"date": "2023-01-15", "payment_mode": "credit_card"}})
    client.post("/models/add_order", json={"user_id": "user123", "order": {"items": [{"title": "Book Title", "price": 19.99, "quantity": 2}]}})
    
    resp = client.post("/models/get_user_purchase_history", json={"user_id":"user123","days_back":730})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "purchase1", "date": "2023-01-15", "payment_mode": "credit_card", "items": [{"title": "Book Title", "price": 19.99, "quantity": 2}]}]

def test_get_user_purchase_history_zero_days():
    # Setup
    client.post("/models/add_purchase", json={"user_id": "user123", "purchase": {"date": "2023-01-15", "payment_mode": "credit_card"}})
    client.post("/models/add_order", json={"user_id": "user123", "order": {"items": [{"title": "Book Title", "price": 19.99, "quantity": 2}]}})
    
    resp = client.post("/models/get_user_purchase_history", json={"user_id":"user123","days_back":0})
    assert resp.status_code == 200
    assert resp.json() == []

def test_get_user_purchase_history_invalid_user_id():
    resp = client.post("/models/get_user_purchase_history", json={"user_id":"","days_back":730})
    assert resp.status_code >= 400

def test_format_purchase_summary_anchor():
    resp = client.post("/views/format_purchase_summary", json={"purchase":{"date":"2023-01-15","payment_mode":"credit_card"}})
    assert resp.status_code == 200
    assert resp.json() == {"date": "2023-01-15", "payment_mode": "credit_card"}

def test_format_purchase_summary_different_payment_mode():
    resp = client.post("/views/format_purchase_summary", json={"purchase":{"date":"2023-06-20","payment_mode":"paypal"}})
    assert resp.status_code == 200
    assert resp.json() == {"date": "2023-06-20", "payment_mode": "paypal"}

def test_format_purchase_summary_empty_purchase():
    resp = client.post("/views/format_purchase_summary", json={"purchase":{}})
    assert resp.status_code >= 400

def test_format_order_items_anchor():
    resp = client.post("/views/format_order_items", json={"items":[{"title":"Book Title","price":19.99,"quantity":2}]})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Book Title", "price": 19.99, "quantity": 2}]

def test_format_order_items_multiple_books():
    resp = client.post("/views/format_order_items", json={"items":[{"title":"Book Title 1","price":19.99,"quantity":2},{"title":"Book Title 2","price":29.99,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Book Title 1", "price": 19.99, "quantity": 2}, {"title": "Book Title 2", "price": 29.99, "quantity": 1}]

def test_format_order_items_single_book():
    resp = client.post("/views/format_order_items", json={"items":[{"title":"Single Book","price":9.99,"quantity":1}]})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Single Book", "price": 9.99, "quantity": 1}]

def test_format_order_items_empty_list():
    resp = client.post("/views/format_order_items", json={"items":[]})
    assert resp.status_code >= 400
