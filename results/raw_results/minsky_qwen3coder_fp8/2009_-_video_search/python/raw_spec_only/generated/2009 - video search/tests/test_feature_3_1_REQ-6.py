"""Spec-derived pytest module for feature 3.1.REQ-6.

Generated black-box from the specification (5 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_fr_3_1_REQ_6_canonical_case():
    resp = client.post("/controllers/fr_3_1_REQ_6", json={"request": {}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_3_1_REQ_6_sort_by_size_asc():
    resp = client.post("/controllers/fr_3_1_REQ_6", json={"request": {"sort_by": "size", "order": "asc"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_3_1_REQ_6_sort_by_date_desc():
    resp = client.post("/controllers/fr_3_1_REQ_6", json={"request": {"sort_by": "date", "order": "desc"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_3_1_REQ_6_sort_by_name_alpha():
    resp = client.post("/controllers/fr_3_1_REQ_6", json={"request": {"sort_by": "name", "order": "asc"}})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_fr_3_1_REQ_6_invalid_sort_column():
    resp = client.post("/controllers/fr_3_1_REQ_6", json={"request": {"sort_by": "invalid_column", "order": "asc"}})
    assert resp.status_code >= 400
