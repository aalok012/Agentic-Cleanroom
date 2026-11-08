"""Spec-derived pytest module for feature 4.3.1.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_display_search_interface_anchor():
    resp = client.post("/views/display_search_interface", json={})
    assert resp.status_code == 200
    assert resp.json() == {"search_fields": ["title", "author", "isbn"]}

def test_display_search_interface_empty_query():
    resp = client.post("/views/display_search_interface", json={})
    assert resp.status_code == 200
    assert resp.json() == {"search_fields": ["title", "author", "isbn"]}

def test_search_books_anchor():
    resp = client.post("/controllers/search_books", json={"query":"Harry Potter"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "isbn": "9780747532699", "cover_image": "https://example.com/harry_potter.jpg", "price": 12.99, "availability": True, "condition": "Good"}]

def test_search_books_empty_query():
    resp = client.post("/controllers/search_books", json={"query":""})
    assert resp.status_code == 200
    assert resp.json() == []

def test_search_books_special_characters():
    resp = client.post("/controllers/search_books", json={"query":"Harry * Potter"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "isbn": "9780747532699", "cover_image": "https://example.com/harry_potter.jpg", "price": 12.99, "availability": True, "condition": "Good"}]

def test_search_books_invalid_query_type():
    resp = client.post("/controllers/search_books", json={"query":123})
    assert resp.status_code >= 400
