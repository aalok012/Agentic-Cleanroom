"""Spec-derived pytest module for feature 3.1.REQ-6.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_sort_torrent_results_anchor_case():
    resp = client.post("/views/sort_torrent_results", json={"results":[{"name":"movie1","size":"1GB","date":"2023-01-01"},{"name":"movie2","size":"2GB","date":"2023-01-02"}],"sort_by":"size"})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "movie1", "size": "1GB", "date": "2023-01-01"}, {"name": "movie2", "size": "2GB", "date": "2023-01-02"}]

def test_sort_torrent_results_by_date():
    resp = client.post("/views/sort_torrent_results", json={"results":[{"name":"movie2","size":"2GB","date":"2023-01-02"},{"name":"movie1","size":"1GB","date":"2023-01-01"}],"sort_by":"date"})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "movie1", "size": "1GB", "date": "2023-01-01"}, {"name": "movie2", "size": "2GB", "date": "2023-01-02"}]

def test_sort_torrent_results_alphabetical():
    resp = client.post("/views/sort_torrent_results", json={"results":[{"name":"movie2","size":"2GB","date":"2023-01-02"},{"name":"movie1","size":"1GB","date":"2023-01-01"}],"sort_by":"alphabetical"})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "movie1", "size": "1GB", "date": "2023-01-01"}, {"name": "movie2", "size": "2GB", "date": "2023-01-02"}]

def test_sort_torrent_results_empty_list():
    resp = client.post("/views/sort_torrent_results", json={"results":[],"sort_by":"size"})
    assert resp.status_code == 200
    assert resp.json() == []

def test_sort_torrent_results_invalid_sort_by():
    resp = client.post("/views/sort_torrent_results", json={"results":[],"sort_by":"invalid_sort"})
    assert resp.status_code >= 400
