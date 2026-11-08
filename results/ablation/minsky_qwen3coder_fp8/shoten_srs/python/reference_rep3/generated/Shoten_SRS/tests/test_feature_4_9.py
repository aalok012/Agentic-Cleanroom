"""Spec-derived pytest module for feature 4.9.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_initiate_book_addition_anchor():
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"user123","user_type":"bookstore"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_initiate_book_addition_failure():
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"","user_type":"bookstore"})
    assert resp.status_code >= 400

def test_validate_and_store_book_details_anchor():
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"Python Programming","quantity":50,"lending_option":True,"selling_option":True,"isbn":"978-0134685991","author":"John Doe","rental_price":5.99,"selling_price":49.99}})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "book_id": "book456"}

def test_validate_and_store_book_details_failure():
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"","quantity":50,"lending_option":True,"selling_option":True,"isbn":"978-0134685991","author":"John Doe","rental_price":5.99,"selling_price":49.99}})
    assert resp.status_code >= 400

def test_store_payment_details_anchor():
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"123456789012","ifsc_code":"HDFC0000123"},"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == True

def test_store_payment_details_failure():
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"","ifsc_code":"HDFC0000123"},"user_id":"user123"})
    assert resp.status_code >= 400
