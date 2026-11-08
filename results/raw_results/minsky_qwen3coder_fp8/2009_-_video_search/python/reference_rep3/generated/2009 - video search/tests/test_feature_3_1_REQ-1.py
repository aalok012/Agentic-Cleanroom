"""Spec-derived pytest module for feature 3.1.REQ-1.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_search_torrents_and_streaming():
    # Test case 1: Canonical case with pizza query
    resp = client.post("/controllers/search_torrents_and_streaming", json={"query":"pizza"})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [{"name": "Pizza Recipe Torrent", "size": "10MB"}], "streaming": [{"title": "Pizza Cooking Show", "provider": "Netflix"}]}

    # Test case 2: Empty query string
    resp = client.post("/controllers/search_torrents_and_streaming", json={"query":""})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}

    # Test case 3: Special characters in query
    resp = client.post("/controllers/search_torrents_and_streaming", json={"query":"movie & series"})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}

    # Test case 4: Query with numbers
    resp = client.post("/controllers/search_torrents_and_streaming", json={"query":"12345"})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}
