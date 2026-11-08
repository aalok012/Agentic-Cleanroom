"""Spec-derived pytest module for feature 3.1.REQ-3.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_anchor_case():
    resp = client.post("/controllers/fr_3_1_REQ_3", json={"request": {"include_torrent_search": True}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_user_disables_torrent_search():
    resp = client.post("/controllers/fr_3_1_REQ_3", json={"request": {"include_torrent_search": False}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_missing_include_torrent_search_field():
    resp = client.post("/controllers/fr_3_1_REQ_3", json={"request": {}})
    assert resp.status_code >= 400

def test_invalid_type_for_include_torrent_search():
    resp = client.post("/controllers/fr_3_1_REQ_3", json={"request": {"include_torrent_search": "true"}})
    assert resp.status_code >= 400
