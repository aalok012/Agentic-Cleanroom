"""Spec-derived pytest module for feature 4.12.

Generated black-box from the specification (7 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_requirement_4_12_REQ_1_anchor():
    resp = client.post("/models/get_user_orders_last_30_days", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == [{"order_id": "order001", "status": "in transit"}, {"order_id": "order002", "status": "delivered"}]

def test_requirement_4_12_REQ_1_independent_no_orders():
    resp = client.post("/models/get_user_orders_last_30_days", json={"user_id":"user456"})
    assert resp.status_code == 200
    assert resp.json() == []

def test_requirement_4_12_REQ_1_failure_empty_user_id():
    resp = client.post("/models/get_user_orders_last_30_days", json={"user_id":""})
    assert resp.status_code >= 400

def test_requirement_4_12_REQ_2_anchor():
    resp = client.post("/models/get_order_by_confirmation_number", json={"confirmation_number":"CONF123456","user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == {"order_id": "order001", "confirmation_number": "CONF123456", "status": "in transit"}

def test_requirement_4_12_REQ_2_failure_invalid_confirmation():
    resp = client.post("/models/get_order_by_confirmation_number", json={"confirmation_number":"INVALID","user_id":"user123"})
    assert resp.status_code >= 400

def test_requirement_4_12_REQ_3_anchor():
    resp = client.post("/views/get_order_shipping_details", json={"order_id":"order001"})
    assert resp.status_code == 200
    assert resp.json() == {"shipping_date": "2023-04-01", "mailing_address": "123 Main St, City, State 12345", "projected_delivery_date": "2023-04-10", "status": "in transit"}

def test_requirement_4_12_REQ_3_failure_invalid_order_id():
    resp = client.post("/views/get_order_shipping_details", json={"order_id":"invalid_order"})
    assert resp.status_code >= 400
