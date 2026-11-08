"""Spec-derived pytest module for feature 4.3.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_search_books_and_print_shops():
    # Test case 1: Search for books and print shops with a valid query
    resp = client.post("/controllers/search_books_and_print_shops", json={"query":"fantasy novels"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "The Hobbit", "type": "book"}, {"name": "PrintZone", "type": "print_shop"}]

    # Test case 2: Search with an empty query string
    resp = client.post("/controllers/search_books_and_print_shops", json={"query":""})
    assert resp.status_code == 200
    assert resp.json() == []

    # Test case 3: Search for a non-existent term
    resp = client.post("/controllers/search_books_and_print_shops", json={"query":"nonexistent book"})
    assert resp.status_code == 200
    assert resp.json() == []

    # Test case 4: Search with special characters in query
    resp = client.post("/controllers/search_books_and_print_shops", json={"query":"science-fiction & fantasy"})
    assert resp.status_code == 200
    assert resp.json() == [{"title": "Dune", "type": "book"}, {"name": "TechPrint", "type": "print_shop"}]
