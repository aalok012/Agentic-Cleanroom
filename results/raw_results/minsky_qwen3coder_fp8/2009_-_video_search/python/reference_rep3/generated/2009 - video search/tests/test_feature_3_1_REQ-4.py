"""Spec-derived pytest module for feature 3.1.REQ-4.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_search_torrents_canonical():
    resp = client.post("/controllers/search_torrents", json={"query":"ubuntu 20.04"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": 150, "peers": 30, "size": "1.2 GB", "date_posted": "2023-05-15", "link": "https://example.com/torrent/ubuntu-20.04.torrent"}]

def test_search_torrents_empty_query():
    resp = client.post("/controllers/search_torrents", json={"query":""})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": 0, "peers": 0, "size": "0 B", "date_posted": "1970-01-01", "link": "https://example.com/torrent/empty.torrent"}]

def test_search_torrents_special_characters():
    resp = client.post("/controllers/search_torrents", json={"query":"ubuntu 20.04 & linux"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": 120, "peers": 25, "size": "1.5 GB", "date_posted": "2023-06-10", "link": "https://example.com/torrent/ubuntu-20.04-linux.torrent"}]

def test_search_torrents_nonexistent():
    resp = client.post("/controllers/search_torrents", json={"query":"nonexistent torrent"})
    assert resp.status_code == 200
    assert resp.json() == []
