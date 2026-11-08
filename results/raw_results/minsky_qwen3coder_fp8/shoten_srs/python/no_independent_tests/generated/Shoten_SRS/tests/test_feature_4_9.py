"""Spec-derived pytest module for feature 4.9.

Generated black-box from the specification (8 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_requirement_4_9_REQ_1_anchor_case():
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"user123","user_type":"bookstore"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_requirement_4_9_REQ_1_independent_user_type():
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"user123","user_type":"customer"})
    assert resp.status_code >= 400

def test_requirement_4_9_REQ_1_independent_empty_user_id():
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"","user_type":"bookstore"})
    assert resp.status_code >= 400

def test_requirement_4_9_REQ_2_anchor_case():
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"Python Programming","quantity":50,"lending_option":True,"selling_option":True,"isbn":"978-0134685991","author":"John Doe","rental_price":5.99,"selling_price":49.99}})
    assert resp.status_code == 200
    assert resp.json() == {"success": True, "errors": []}

def test_requirement_4_9_REQ_2_independent_missing_fields():
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"","quantity":0,"lending_option":True,"selling_option":True,"isbn":"","author":"","rental_price":0,"selling_price":0}})
    assert resp.status_code >= 400

def test_requirement_4_9_REQ_2_independent_invalid_values():
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"Test Book","quantity":-5,"lending_option":True,"selling_option":True,"isbn":"1234567890123","author":"Author Name","rental_price":-2.99,"selling_price":-10.99}})
    assert resp.status_code >= 400

def test_requirement_4_9_REQ_3_anchor_case():
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"123456789012","ifsc_code":"HDFC0000123"}})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Payment details stored successfully"}

def test_requirement_4_9_REQ_3_independent_missing_fields():
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"","ifsc_code":""}})
    assert resp.status_code >= 400
