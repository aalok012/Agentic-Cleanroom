"""Spec-derived pytest module for feature 3.1.REQ-7.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_paginate_search_results_anchor_case():
    resp = client.post("/views/paginate_search_results", json={"page_number":2,"page_size":10,"search_query":"linux"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "ubuntu-20.04.iso", "size": "2.3GB"}, {"name": "fedora-34.iso", "size": "1.8GB"}], "page": 2, "total_pages": 5}

def test_paginate_search_results_first_page():
    resp = client.post("/views/paginate_search_results", json={"page_number":1,"page_size":10,"search_query":"linux"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "debian-11.iso", "size": "2.1GB"}, {"name": "arch-linux.iso", "size": "1.9GB"}], "page": 1, "total_pages": 5}

def test_paginate_search_results_last_page():
    resp = client.post("/views/paginate_search_results", json={"page_number":5,"page_size":10,"search_query":"linux"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "gentoo-2021.iso", "size": "2.5GB"}], "page": 5, "total_pages": 5}

def test_paginate_search_results_invalid_page_zero():
    resp = client.post("/views/paginate_search_results", json={"page_number":0,"page_size":10,"search_query":"linux"})
    assert resp.status_code >= 400
