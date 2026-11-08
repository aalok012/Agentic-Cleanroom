"""Spec-derived pytest module for feature 3.1.REQ-1.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_canonical_case():
    resp = client.post("/search", json={"query": "pizza"})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}

def test_empty_query():
    resp = client.post("/search", json={"query": ""})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}

def test_special_characters():
    resp = client.post("/search", json={"query": "!@#$%^&*()"})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}

def test_long_query():
    resp = client.post("/search", json={"query": "a" * 1000})
    assert resp.status_code == 200
    assert resp.json() == {"torrents": [], "streaming": []}
