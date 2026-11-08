"""Spec-derived pytest module for feature 3.2.REQ-12.

Generated black-box from the specification (1 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from app import create_app

client = TestClient(create_app())

def test_fr_3_2_REQ_12_anchor_case():
    # Anchor case: Simple Interface for easy and reliable interactivity with no inputs.
    resp = client.post("/controllers/fr_3_2_REQ_12", json={})
    assert resp.status_code == 200
    assert resp.json() is None
