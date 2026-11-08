"""Spec-derived pytest module for feature 4.5.

Generated black-box from the specification (7 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_remove_book_from_cart():
    # Setup: Add a book to cart
    client.post("/controllers/add_to_cart", json={"action": "add", "cart_item": {"user_id": 123, "book_id": 456}})
    
    # Test anchor case
    resp = client.post("/controllers/remove_book_from_cart", json={"user_id":123,"book_id":456})
    assert resp.status_code == 200
    assert resp.json() is None
    
    # Test failure case
    resp = client.post("/controllers/remove_book_from_cart", json={"user_id":0,"book_id":456})
    assert resp.status_code >= 400

def test_select_book_for_deletion():
    # Setup: Add a book to cart
    client.post("/controllers/add_to_cart", json={"action": "add", "cart_item": {"user_id": 123, "book_id": 456}})
    
    # Test anchor case
    resp = client.post("/controllers/select_book_for_deletion", json={"user_id":123,"book_id":456})
    assert resp.status_code == 200
    assert resp.json() == {"user_id": 123, "book_id": 456}
    
    # Test failure case
    resp = client.post("/controllers/select_book_for_deletion", json={"user_id":0,"book_id":456})
    assert resp.status_code >= 400

def test_update_cart_after_deletion():
    # Setup: Add books to cart
    client.post("/controllers/add_to_cart", json={"action": "add", "cart_item": {"user_id": 123, "book_id": 456}})
    client.post("/controllers/add_to_cart", json={"action": "add", "cart_item": {"user_id": 123, "book_id": 789}})
    
    # Test anchor case
    resp = client.post("/controllers/update_cart_after_deletion", json={"user_id":123,"book_id":456})
    assert resp.status_code == 200
    assert resp.json() == [{"book_id": 789, "title": "Book Title"}]
    
    # Test edge case: delete last book
    client.post("/controllers/add_to_cart", json={"action": "add", "cart_item": {"user_id": 123, "book_id": 456}})
    resp = client.post("/controllers/update_cart_after_deletion", json={"user_id":123,"book_id":456})
    assert resp.status_code == 200
    assert resp.json() == []
    
    # Test failure case
    resp = client.post("/controllers/update_cart_after_deletion", json={"user_id":0,"book_id":456})
    assert resp.status_code >= 400
