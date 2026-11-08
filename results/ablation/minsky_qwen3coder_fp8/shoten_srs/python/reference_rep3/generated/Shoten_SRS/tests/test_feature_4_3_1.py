"""Spec-derived pytest module for feature 4.3.1.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_display_book_search_interface_anchor():
    resp = client.post("/views/display_book_search_interface", json={})
    assert resp.status_code == 200
    assert resp.json() == {"interface": "book_search", "fields": ["title", "author", "isbn"]}

def test_display_book_search_interface_empty_fields():
    resp = client.post("/views/display_book_search_interface", json={"title": "", "author": "", "isbn": ""})
    assert resp.status_code == 200
    assert resp.json() == {"interface": "book_search", "fields": ["title", "author", "isbn"]}

def test_search_books_anchor():
    resp = client.post("/controllers/search_books", json={"title":"The Great Gatsby","author":"F. Scott Fitzgerald","isbn":"9780743273565"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "cover_image": "https://example.com/cover.jpg", "price": "$12.99", "availability": "In Stock", "condition": "Good"}]

def test_search_books_title_only():
    resp = client.post("/controllers/search_books", json={"title":"The Great Gatsby"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "cover_image": "https://example.com/cover.jpg", "price": "$12.99", "availability": "In Stock", "condition": "Good"}]

def test_search_books_author_only():
    resp = client.post("/controllers/search_books", json={"author":"F. Scott Fitzgerald"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "cover_image": "https://example.com/cover.jpg", "price": "$12.99", "availability": "In Stock", "condition": "Good"}]

def test_search_books_isbn_only():
    resp = client.post("/controllers/search_books", json={"isbn":"9780743273565"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "cover_image": "https://example.com/cover.jpg", "price": "$12.99", "availability": "In Stock", "condition": "Good"}]
