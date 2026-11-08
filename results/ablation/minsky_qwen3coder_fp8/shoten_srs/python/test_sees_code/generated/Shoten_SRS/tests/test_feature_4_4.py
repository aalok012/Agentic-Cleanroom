"""Spec-derived pytest module for feature 4.4.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_add_book_to_cart():
    # Test case 1: Add a book to cart with valid user and book IDs
    resp = client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"book456"})
    assert resp.status_code == 200
    assert resp.json() is None

    # Test case 2: Attempt to add a book to cart with invalid user ID
    resp = client.post("/controllers/add_book_to_cart", json={"user_id":"invalid_user","book_id":"book456"})
    assert resp.status_code >= 400

    # Test case 3: Attempt to add a non-existent book to cart
    resp = client.post("/controllers/add_book_to_cart", json={"user_id":"user123","book_id":"nonexistent_book"})
    assert resp.status_code >= 400

def test_get_cart_total_price():
    # Setup: Add a book to cart first
    client.post("/controllers/add_book_to_cart", json={"user_id":"user123", "book_id":"book456"})

    # Test case 4: Get total price of cart with items
    resp = client.post("/views/get_cart_total_price", json={"user_id":"user123"})
    assert resp.status_code == 200
    assert resp.json() == 49.97

    # Test case 5: Attempt to get total price of empty cart
    resp = client.post("/views/get_cart_total_price", json={"user_id":"user123"})
    assert resp.status_code >= 400

    # Test case 6: Attempt to get total price with empty user ID
    resp = client.post("/views/get_cart_total_price", json={"user_id":""})
    assert resp.status_code >= 400
