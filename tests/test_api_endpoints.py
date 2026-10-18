"""
tests/test_api_endpoints.py - API Endpoints & Contract Integration Tests
"""

import base64
import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["database_connected"] is True
    assert "opencv_version" in data

def test_list_doctors_endpoint(client):
    response = client.get("/api/doctors")
    assert response.status_code == 200
    doctors = response.json()
    assert len(doctors) == 7
    for doc in doctors:
        assert "name" in doc
        assert "specialty" in doc
        assert "rating" in doc

def test_scan_and_dispatch_full_workflow(client):
    # Load sample laceration image
    with open("static/samples/laceration.jpg", "rb") as f:
        raw_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

    scan_resp = client.post("/api/scan", json={
        "image_base64": raw_b64,
        "hint_type": "laceration"
    })
    assert scan_resp.status_code == 200
    scan_data = scan_resp.json()

    assert "triage_id" in scan_data
    assert "patient_ticket" in scan_data
    assert scan_data["injury_type"] == "Deep Dermal Laceration"
    assert len(scan_data["recommended_doctors"]) >= 1

    # Dispatch primary doctor
    chosen_doctor = scan_data["recommended_doctors"][0]
    assign_resp = client.post("/api/assign", json={
        "triage_id": scan_data["triage_id"],
        "doctor_id": chosen_doctor["id"]
    })
    assert assign_resp.status_code == 200
    assign_data = assign_resp.json()
    assert assign_data["status"] == "success"
    assert assign_data["doctor"]["id"] == chosen_doctor["id"]

def test_malformed_image_payload_validation(client):
    response = client.post("/api/scan", json={
        "image_base64": "invalid_truncated_stream"
    })
    # Must be cleanly rejected by RFC 7807 problem details handler or Pydantic validation
    assert response.status_code in [400, 422]
