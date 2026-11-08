"""Spec-derived pytest module for feature 4.5.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_remove_book_from_cart_anchor():
    # Setup: Add book to cart
    client.post("/controllers/add_to_cart", json={"user_id":"user123","book_id":"book456"})
    
    # Main test
    resp = client.post("/controllers/remove_book_from_cart", json={"user_id":"user123","book_id":"book456"})
    assert resp.status_code == 200
    assert resp.json() is None

def test_remove_book_from_cart_failure():
    resp = client.post("/controllers/remove_book_from_cart", json={"user_id":"","book_id":"book456"})
    assert resp.status_code >= 400

def test_select_book_for_deletion_anchor():
    # Setup: Add book to cart
    client.post("/controllers/add_to_cart", json={"user_id":"user123","book_id":"book456"})
    
    # Main test
    resp = client.post("/controllers/select_book_for_deletion", json={"user_id":"user123","book_id":"book456"})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Book selected for deletion"}

def test_select_book_for_deletion_failure():
    resp = client.post("/controllers/select_book_for_deletion", json={"user_id":"","book_id":"book456"})
    assert resp.status_code >= 400

def test_update_cart_after_deletion_anchor():
    # Setup: Add books to cart
    client.post("/controllers/add_to_cart", json={"user_id":"user123","book_id":"book456"})
    client.post("/controllers/add_to_cart", json={"user_id":"user123","book_id":"book789"})
    
    # Main test
    resp = client.post("/controllers/update_cart_after_deletion", json={"user_id":"user123","book_id":"book456"})
    assert resp.status_code == 200
    assert resp.json() == [{"id": "book789", "title": "Another Book"}]

def test_update_cart_after_deletion_failure():
    resp = client.post("/controllers/update_cart_after_deletion", json={"user_id":"","book_id":"book456"})
    assert resp.status_code >= 400
