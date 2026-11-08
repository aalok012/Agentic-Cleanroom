"""Spec-derived pytest module for feature 3.1.REQ-4.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
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
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]

def test_search_torrents_empty_query():
    resp = client.post("/controllers/search_torrents", json={"query":""})
    assert resp.status_code >= 400

def test_search_torrents_special_characters():
    client.post("/controllers/add_torrent", json={"action": "add", "torrent": {"name": "ubuntu 20.04 LTS", "seeds": 150, "peers": 30, "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}})
    resp = client.post("/controllers/search_torrents", json={"query":"ubuntu 20.04 LTS"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]

def test_search_torrents_no_matches():
    resp = client.post("/controllers/search_torrents", json={"query":"nonexistent_file"})
    assert resp.status_code >= 400

def test_search_torrents_case_insensitive():
    client.post("/controllers/add_torrent", json={"action": "add", "torrent": {"name": "ubuntu 20.04", "seeds": 150, "peers": 30, "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}})
    resp = client.post("/controllers/search_torrents", json={"query":"UBUNTU 20.04"})
    assert resp.status_code == 200
    assert resp.json() == [{"seeds": "150", "peers": "30", "size": "2.3 GB", "date_posted": "2023-05-15", "webpage_link": "https://example.com/torrent/ubuntu-20.04"}]
