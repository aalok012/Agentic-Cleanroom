"""Spec-derived pytest module for feature 4.12.

Generated black-box from the specification (7 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_req_1_anchor():
    # Setup: Add an order for user123
    client.post("/models/add_order", json={"action": "add", "order": {"order_id": "order456", "user_id": "user123", "date_placed": "2023-03-01"}})
    
    resp = client.post("/models/get_user_orders_in_last_30_days", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == [{"order_id": "order456", "status": "in transit"}]

def test_req_1_empty_orders():
    # Setup: Add an old order for user123
    client.post("/models/add_order", json={"action": "add", "order": {"order_id": "order789", "user_id": "user123", "date_placed": "2023-02-01"}})
    
    resp = client.post("/models/get_user_orders_in_last_30_days", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == []

def test_req_1_failure():
    resp = client.post("/models/get_user_orders_in_last_30_days", json={"user_id":""})
    assert resp.status_code >= 400

def test_req_2_anchor():
    # Setup: Add an order with confirmation number
    client.post("/models/add_order", json={"action": "add", "order": {"order_id": "order456", "confirmation_number": "CONF123456", "user_id": "user123", "shipping_date": "2023-04-01", "delivery_address": "123 Main St", "projected_delivery_date": "2023-04-10", "status": "in transit"}})
    
    resp = client.post("/models/get_order_by_confirmation_number", json={"confirmation_number":"CONF123456","user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"order_id": "order456", "status": "in transit", "shipping_date": "2023-04-01", "delivery_address": "123 Main St", "projected_delivery_date": "2023-04-10"}

def test_req_2_invalid_confirmation():
    resp = client.post("/models/get_order_by_confirmation_number", json={"confirmation_number":"INVALID","user_id":"user123"})
    assert resp.status_code >= 400

def test_req_3_anchor():
    resp = client.post("/views/display_order_shipping_details", json={"order":{"shipping_date":"2023-04-01","delivery_address":"123 Main St","projected_delivery_date":"2023-04-10","status":"in transit"}})
    assert resp.status_code == 200
    assert resp.json() == {"shipping_date": "2023-04-01", "delivery_address": "123 Main St", "projected_delivery_date": "2023-04-10", "status": "in transit"}

def test_req_3_missing_fields():
    resp = client.post("/views/display_order_shipping_details", json={"order":{}})
    assert resp.status_code >= 400
