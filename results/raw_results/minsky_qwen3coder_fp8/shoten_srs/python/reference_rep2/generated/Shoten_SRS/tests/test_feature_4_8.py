"""Spec-derived pytest module for feature 4.8.

Generated black-box from the specification (12 case(s)); the Test Agent never sees the implementation, so import paths follow
sensible module conventions and may need adjustment to bind to the concrete
generated package.
"""

import json
from fastapi.testclient import TestClient
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app import create_app

client = TestClient(create_app())

def test_req_1_anchor():
    resp = client.post("/controllers/initiate_print_request", json={"user_id":"user123","print_shop_id":"shop456"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "initiated", "message": "Print request process started for print shop shop456"}

def test_req_1_failure():
    resp = client.post("/controllers/initiate_print_request", json={"user_id":"","print_shop_id":"shop456"})
    assert resp.status_code >= 400

def test_req_2_anchor():
    resp = client.post("/views/prompt_google_drive_url", json={"print_job_id":"job789"})
    assert resp.status_code == 200
    assert resp.json() == {"prompt": "Please enter the Google Drive link URL of the document to be printed"}

def test_req_2_failure():
    resp = client.post("/views/prompt_google_drive_url", json={"print_job_id":""})
    assert resp.status_code >= 400

def test_req_3_anchor():
    resp = client.post("/models/calculate_print_cost", json={"google_drive_url":"https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0j/view"})
    assert resp.status_code == 200
    assert resp.json() == {"total_cost": 12.5}

def test_req_3_failure():
    resp = client.post("/models/calculate_print_cost", json={"google_drive_url":"invalid-url"})
    assert resp.status_code >= 400

def test_req_4_anchor():
    resp = client.post("/controllers/collect_delivery_information_4_8_REQ_4", json={"print_job_id":"job789","delivery_info":{"street":"123 Main St","city":"Anytown","zip":"12345"}})
    assert resp.status_code == 200
    assert resp.json() == {"status": "collected", "message": "Delivery information successfully recorded"}

def test_req_4_failure():
    resp = client.post("/controllers/collect_delivery_information_4_8_REQ_4", json={"print_job_id":"job789","delivery_info":{}})
    assert resp.status_code >= 400

def test_req_5_anchor():
    resp = client.post("/views/prompt_payment_information_4_8_REQ_5", json={"print_job_id":"job789"})
    assert resp.status_code == 200
    assert resp.json() == {"prompt": "Please enter your payment information to complete the transaction"}

def test_req_5_failure():
    resp = client.post("/views/prompt_payment_information_4_8_REQ_5", json={"print_job_id":""})
    assert resp.status_code >= 400

def test_req_6_anchor():
    resp = client.post("/views/display_delivery_status", json={"print_job_id":"job789"})
    assert resp.status_code == 200
    assert resp.json() == {"status": "shipped", "tracking_number": "TRK123456789"}

def test_req_6_failure():
    resp = client.post("/views/display_delivery_status", json={"print_job_id":""})
    assert resp.status_code >= 400
