"""
tests/test_database.py - Database Layer Integration Tests
"""

import pytest
import os
from database import DatabaseManager

@pytest.fixture
def temp_db(tmp_path):
    test_db_path = str(tmp_path / "test_receptionist.db")
    mgr = DatabaseManager(db_path=test_db_path)
    mgr.initialize_schema()
    return mgr

def test_database_initialization_and_seeding(temp_db):
    doctors = temp_db.fetch_all_doctors()
    assert len(doctors) == 7
    assert any(d["specialty"] == "Trauma & Emergency" for d in doctors)
    assert any(d["specialty"] == "Orthopedic Surgery" for d in doctors)

def test_specialist_lookup_matching(temp_db):
    burn_specialists = temp_db.find_specialists("Burn Care")
    assert len(burn_specialists) >= 1
    assert "Burn" in burn_specialists[0]["specialty"] or "Burn" in burn_specialists[0]["sub_specialty"]

def test_triage_logging_and_assignment_lifecycle(temp_db):
    # Log admission ticket
    triage_id, ticket_num = temp_db.record_triage(
        injury_type="Deep Dermal Laceration",
        severity="Urgent",
        confidence=0.95,
        specialty_needed="Trauma & Emergency",
        first_aid="Direct pressure | Sterile dressing",
        doctor_id=None
    )
    assert triage_id > 0
    assert ticket_num.startswith("ER-")

    # Dispatch doctor
    doctors = temp_db.fetch_all_doctors()
    target_doc = doctors[0]
    assignment = temp_db.assign_doctor(triage_id, target_doc["id"])

    assert assignment["ticket_num"] == ticket_num
    assert assignment["doctor"]["id"] == target_doc["id"]

    # Verify history
    history = temp_db.fetch_recent_scans(limit=5)
    assert len(history) == 1
    assert history[0]["patient_ticket"] == ticket_num
    assert history[0]["doctor_assigned_id"] == target_doc["id"]
