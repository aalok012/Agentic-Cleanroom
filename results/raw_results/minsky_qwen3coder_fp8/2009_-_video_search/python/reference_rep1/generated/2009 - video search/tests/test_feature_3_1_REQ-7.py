"""Spec-derived pytest module for feature 3.1.REQ-7.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_paginate_search_results():
    # Test case 1: Canonical case
    resp = client.post("/views/paginate_search_results", json={"page_number":1,"page_size":10,"search_query":"ubuntu"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "ubuntu-20.04.iso", "size": "1.5GB"}, {"name": "ubuntu-20.04-live.iso", "size": "800MB"}]}

    # Test case 2: Page 2
    resp = client.post("/views/paginate_search_results", json={"page_number":2,"page_size":10,"search_query":"ubuntu"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "ubuntu-22.04.iso", "size": "2.0GB"}, {"name": "ubuntu-22.04-live.iso", "size": "900MB"}]}

    # Test case 3: Boundary case with page size 1
    resp = client.post("/views/paginate_search_results", json={"page_number":1,"page_size":1,"search_query":"ubuntu"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "ubuntu-20.04.iso", "size": "1.5GB"}]}

    # Test case 4: Invalid negative page number
    resp = client.post("/views/paginate_search_results", json={"page_number":-1,"page_size":10,"search_query":"ubuntu"})
    assert resp.status_code >= 400

    # Test case 5: Empty search query
    resp = client.post("/views/paginate_search_results", json={"page_number":1,"page_size":10,"search_query":""})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "empty-search-result-1.iso", "size": "100MB"}, {"name": "empty-search-result-2.iso", "size": "200MB"}]}
