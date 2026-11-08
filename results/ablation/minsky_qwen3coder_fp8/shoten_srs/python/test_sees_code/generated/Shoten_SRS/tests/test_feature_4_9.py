"""Spec-derived pytest module for feature 4.9.

Generated black-box from the specification (9 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_initiate_book_addition():
    # Test anchor case
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"user123","user_type":"bookstore"})
    assert resp.status_code == 200
    assert resp.json() == True
    
    # Test failure case - invalid user ID
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"","user_type":"bookstore"})
    assert resp.status_code >= 400
    
    # Test failure case - invalid user type
    resp = client.post("/controllers/initiate_book_addition", json={"user_id":"user123","user_type":"invalid_type"})
    assert resp.status_code >= 400

def test_validate_and_store_book_details():
    # Test anchor case
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"Python Programming","quantity":50,"lending_option":true,"selling_option":true,"isbn":"978-0134685991","author":"John Doe","rental_price":5.99,"selling_price":49.99}})
    assert resp.status_code == 200
    assert resp.json() == {"success": True, "errors": []}
    
    # Test failure case - missing required fields
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"","quantity":0,"lending_option":true,"selling_option":true,"isbn":"","author":"","rental_price":0,"selling_price":0}})
    assert resp.status_code >= 400
    
    # Test failure case - invalid data types
    resp = client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":123,"quantity":"invalid","lending_option":"true","selling_option":true,"isbn":null,"author":123,"rental_price":"invalid","selling_price":-10}})
    assert resp.status_code >= 400

def test_store_payment_details():
    # First create a book addition record
    client.post("/controllers/initiate_book_addition", json={"user_id":"user123","user_type":"bookstore"})
    client.post("/controllers/validate_and_store_book_details", json={"book_data":{"name":"Python Programming","quantity":50,"lending_option":true,"selling_option":true,"isbn":"978-0134685991","author":"John Doe","rental_price":5.99,"selling_price":49.99}})
    
    # Test anchor case
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"123456789012","ifsc_code":"HDFC0000123"}})
    assert resp.status_code == 200
    assert resp.json() == {"status": "success", "message": "Payment details stored successfully"}
    
    # Test failure case - incomplete payment info
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"","ifsc_code":""}})
    assert resp.status_code >= 400
    
    # Test failure case - user hasn't completed book details
    client.post("/controllers/initiate_book_addition", json={"user_id":"user456","user_type":"bookstore"})
    resp = client.post("/controllers/store_payment_details", json={"payment_info":{"bank_account_number":"123456789012","ifsc_code":"HDFC0000123","user_id":"user456"}})
    assert resp.status_code >= 400
