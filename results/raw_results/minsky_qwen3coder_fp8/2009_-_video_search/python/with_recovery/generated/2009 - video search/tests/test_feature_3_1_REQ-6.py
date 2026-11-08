"""Spec-derived pytest module for feature 3.1.REQ-6.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_sort_torrent_results_by_size():
    resp = client.post("/views/sort_torrent_results", json={"results":[{"name":"file1","size":"10MB","date":"2023-01-01"},{"name":"file2","size":"5MB","date":"2023-01-02"}],"sort_by":"size"})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "file1", "size": "10MB", "date": "2023-01-01"}, {"name": "file2", "size": "5MB", "date": "2023-01-02"}]

def test_sort_torrent_results_by_date():
    resp = client.post("/views/sort_torrent_results", json={"results":[{"name":"file2","size":"5MB","date":"2023-01-02"},{"name":"file1","size":"10MB","date":"2023-01-01"}],"sort_by":"date"})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "file1", "size": "10MB", "date": "2023-01-01"}, {"name": "file2", "size": "5MB", "date": "2023-01-02"}]

def test_sort_torrent_results_alphabetically():
    resp = client.post("/views/sort_torrent_results", json={"results":[{"name":"file2","size":"5MB","date":"2023-01-02"},{"name":"file1","size":"10MB","date":"2023-01-01"}],"sort_by":"alphabetical"})
    assert resp.status_code == 200
    assert resp.json() == [{"name": "file1", "size": "10MB", "date": "2023-01-01"}, {"name": "file2", "size": "5MB", "date": "2023-01-02"}]

def test_sort_torrent_results_invalid_sort_by():
    resp = client.post("/views/sort_torrent_results", json={"results":[],"sort_by":"invalid"})
    assert resp.status_code >= 400
