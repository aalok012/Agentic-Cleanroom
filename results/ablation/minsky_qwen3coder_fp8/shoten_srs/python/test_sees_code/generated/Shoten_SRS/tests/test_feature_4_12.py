"""Spec-derived pytest module for feature 4.12.

Generated black-box from the specification (7 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_get_user_orders_in_last_30_days_anchor():
    # Setup
    client.post("/models/get_user_orders_in_last_30_days", json={"user_id": "user123", "order_id": "order456", "status": "in transit", "created_at": "2023-03-01T00:00:00Z"})
    
    # Test
    resp = client.post("/models/get_user_orders_in_last_30_days", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == [{"order_id": "order456", "status": "in transit"}]

def test_get_user_orders_in_last_30_days_no_recent_orders():
    # Test
    resp = client.post("/models/get_user_orders_in_last_30_days", json={"user_id":"user456"})
    assert resp.status_code == 200
    assert resp.json() == []

def test_get_user_orders_in_last_30_days_invalid_user_id():
    # Test
    resp = client.post("/models/get_user_orders_in_last_30_days", json={"user_id":""})
    assert resp.status_code >= 400

def test_get_order_by_confirmation_number_anchor():
    # Setup
    client.post("/models/get_order_by_confirmation_number", json={"confirmation_number": "CONF123456", "user_id": "user123", "order_id": "order456", "status": "in transit", "shipping_date": "2023-04-01", "delivery_address": "123 Main St", "projected_delivery_date": "2023-04-10"})
    
    # Test
    resp = client.post("/models/get_order_by_confirmation_number", json={"confirmation_number":"CONF123456","user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"order_id": "order456", "status": "in transit", "shipping_date": "2023-04-01", "delivery_address": "123 Main St", "projected_delivery_date": "2023-04-10"}

def test_get_order_by_confirmation_number_invalid_confirmation():
    # Test
    resp = client.post("/models/get_order_by_confirmation_number", json={"confirmation_number":"INVALID","user_id":"user123"})
    assert resp.status_code >= 400

def test_display_order_shipping_details_anchor():
    # Test
    resp = client.post("/views/display_order_shipping_details", json={"order":{"shipping_date":"2023-04-01","delivery_address":"123 Main St","projected_delivery_date":"2023-04-10","status":"in transit"}})
    assert resp.status_code == 200
    assert resp.json() == {"shipping_date": "2023-04-01", "delivery_address": "123 Main St", "projected_delivery_date": "2023-04-10", "status": "in transit"}

def test_display_order_shipping_details_missing_fields():
    # Test
    resp = client.post("/views/display_order_shipping_details", json={"order":{}})
    assert resp.status_code >= 400
