"""Spec-derived pytest module for feature 3.1.REQ-4.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_search_torrents_canonical_case():
    resp = client.post("/controllers/search_torrents", json={"query":"ubuntu 20.04"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]

def test_search_torrents_empty_query():
    resp = client.post("/controllers/search_torrents", json={"query":""})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]

def test_search_torrents_special_characters():
    resp = client.post("/controllers/search_torrents", json={"query":"ubuntu 20.04 & LTS"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]

def test_search_torrents_nonexistent_query():
    resp = client.post("/controllers/search_torrents", json={"query":"nonexistentfile123"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]
