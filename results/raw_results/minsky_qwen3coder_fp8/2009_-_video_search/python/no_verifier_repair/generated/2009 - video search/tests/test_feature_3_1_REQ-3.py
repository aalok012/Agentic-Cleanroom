"""Spec-derived pytest module for feature 3.1.REQ-3.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_toggle_torrent_search_anchor_case():
    resp = client.post("/controllers/toggle_torrent_search", json={"include_torrents": True})
    assert resp.status_code == 200
    assert resp.json() is None

def test_toggle_torrent_search_disable():
    resp = client.post("/controllers/toggle_torrent_search", json={"include_torrents": False})
    assert resp.status_code == 200
    assert resp.json() is None

def test_toggle_torrent_search_invalid_input_type():
    resp = client.post("/controllers/toggle_torrent_search", json={"include_torrents": "invalid"})
    assert resp.status_code >= 400

def test_toggle_torrent_search_missing_field():
    resp = client.post("/controllers/toggle_torrent_search", json={})
    assert resp.status_code >= 400
