"""Spec-derived pytest module for feature 3.1.REQ-7.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
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
    assert resp.json() == {"results": [{"name": "ubuntu-20.04.iso", "size": "1.2GB"}, {"name": "fedora-33.iso", "size": "1.5GB"}]}

def test_paginate_search_results_boundary_first_page():
    resp = client.post("/views/paginate_search_results", json={"page_number":1,"page_size":10,"search_query":"linux"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "ubuntu-20.04.iso", "size": "1.2GB"}, {"name": "fedora-33.iso", "size": "1.5GB"}]}

def test_paginate_search_results_edge_min_page_size():
    resp = client.post("/views/paginate_search_results", json={"page_number":2,"page_size":1,"search_query":"linux"})
    assert resp.status_code == 200
    assert resp.json() == {"results": [{"name": "ubuntu-20.04.iso", "size": "1.2GB"}]}

def test_paginate_search_results_failure_negative_page_number():
    resp = client.post("/views/paginate_search_results", json={"page_number":-1,"page_size":10,"search_query":"linux"})
    assert resp.status_code >= 400

def test_paginate_search_results_failure_zero_page_size():
    resp = client.post("/views/paginate_search_results", json={"page_number":1,"page_size":0,"search_query":"linux"})
    assert resp.status_code >= 400
