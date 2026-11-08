"""Spec-derived pytest module for feature 4.2.

Generated black-box from the specification (6 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_login_user():
    # Setup: Create a user first
    client.post("/controllers/register_user", json={"username": "johndoe", "password": "secret123"})
    
    # Test case 1: Successful login
    resp = client.post("/controllers/login_user", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == True
    
    # Test case 2: Invalid password
    resp = client.post("/controllers/login_user", json={"username":"johndoe","password":"wrongpass"})
    assert resp.status_code >= 400

def test_validate_login_credentials():
    # Test case 3: Missing username
    resp = client.post("/controllers/validate_login_credentials", json={"username":"","password":"secret123"})
    assert resp.status_code >= 400
    
    # Test case 4: Missing password
    resp = client.post("/controllers/validate_login_credentials", json={"username":"johndoe","password":""})
    assert resp.status_code >= 400

def test_verify_credentials():
    # Setup: Create a user first
    client.post("/controllers/register_user", json={"username": "johndoe", "password": "secret123"})
    
    # Test case 5: Valid credentials
    resp = client.post("/models/verify_credentials", json={"username":"johndoe","password":"secret123"})
    assert resp.status_code == 200
    assert resp.json() == True
    
    # Test case 6: Invalid password
    resp = client.post("/models/verify_credentials", json={"username":"johndoe","password":"wrongpass"})
    assert resp.status_code == 200
    assert resp.json() == False
