"""Spec-derived pytest module for feature 4.14.

Generated black-box from the specification (1 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_logout_user_success():
    """Test successful user logout"""
    resp = client.post("/controllers/logout_user", json={})
    assert resp.status_code == 200
    assert resp.json() == {"message": "User logged out successfully"}
