"""Spec-derived pytest module for feature 4.4.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_add_book_to_cart_valid_input():
    resp = client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"book456"})
    assert resp.status_code == 200
    assert resp.json() is None

def test_add_book_to_cart_empty_user_id():
    resp = client.post("/controllers/add_book_to_cart", json={"user_id":"","book_id":"book456"})
    assert resp.status_code >= 400

def test_add_multiple_books_to_cart():
    # First, add a book
    client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"book456"})
    # Then, add another book
    resp = client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"book789"})
    assert resp.status_code == 200
    assert resp.json() is None

def test_get_cart_total_price_valid_input():
    # Setup: Add books to cart
    client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"book456"})
    client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"book789"})
    
    resp = client.post("/views/get_cart_total_price", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == 49.97

def test_get_cart_total_price_empty_user_id():
    resp = client.post("/views/get_cart_total_price", json={"user_id":""})
    assert resp.status_code >= 400
