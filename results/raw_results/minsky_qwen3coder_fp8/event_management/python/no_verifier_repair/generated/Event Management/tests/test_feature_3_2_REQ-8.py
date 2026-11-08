"""Spec-derived pytest module for feature 3.2.REQ-8.

Generated black-box from the specification (4 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_check_admin_access_anchor_case():
    resp = client.post("/controllers/check_admin_access", json={"user_credentials":{"username":"admin_user","password":"secure_password"}})
    assert resp.status_code == 200
    assert resp.json() == True

def test_check_admin_access_non_admin_user():
    resp = client.post("/controllers/check_admin_access", json={"user_credentials":{"username":"regular_user","password":"user_password"}})
    assert resp.status_code == 200
    assert resp.json() == False

def test_check_admin_access_empty_credentials():
    resp = client.post("/controllers/check_admin_access", json={"user_credentials":{"username":"","password":""}})
    assert resp.status_code >= 400

def test_check_admin_access_wrong_password():
    resp = client.post("/controllers/check_admin_access", json={"user_credentials":{"username":"admin_user","password":"wrong_password"}})
    assert resp.status_code == 200
    assert resp.json() == False
