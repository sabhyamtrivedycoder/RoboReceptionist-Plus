"""
run_tests.py - Standard Library Automated Clinical Test Runner
Executes unit tests for CV feature extractor, database transactional manager, and API contracts.
"""

import unittest
import numpy as np
import cv2
import base64
import os
import tempfile
import shutil

from cv_engine import OpticalFeatureExtractor, ClinicalHeuristicClassifier
from database import DatabaseManager
from core.exceptions import ImageDecodingError
from fastapi.testclient import TestClient
from app import app

class TestOpticalPipeline(unittest.TestCase):
    def setUp(self):
        self.extractor = OpticalFeatureExtractor()
        # Create synthetic wound image (240x240 with red lesion)
        self.img = np.ones((240, 240, 3), dtype=np.uint8) * 190
        cv2.circle(self.img, (120, 120), 45, (20, 20, 230), -1)
        cv2.line(self.img, (90, 120), (150, 120), (10, 10, 140), 3)

    def test_base64_roundtrip(self):
        b64 = self.extractor.encode_cv2_to_base64(self.img)
        self.assertTrue(b64.startswith("data:image/jpeg;base64,"))
        decoded = self.extractor.decode_base64_to_cv2(b64)
        self.assertEqual(decoded.shape, self.img.shape)

    def test_malformed_base64_rejection(self):
        with self.assertRaises(ImageDecodingError):
            self.extractor.decode_base64_to_cv2("corrupted_payload_123")

    def test_telemetry_extraction(self):
        telemetry = self.extractor.extract_telemetry(self.img)
        self.assertIn("redness_index", telemetry)
        self.assertIn("edge_density", telemetry)
        self.assertIn("bbox", telemetry)
        self.assertGreater(telemetry["redness_index"], 4.0)
        self.assertIsNotNone(telemetry["bbox"])

    def test_heuristic_classifiers(self):
        burn = ClinicalHeuristicClassifier.classify({"redness_index": 22.0, "edge_density": 3.0})
        self.assertEqual(burn["injury_type"], "Second-Degree Thermal Burn")
        self.assertEqual(burn["recommended_specialty"], "Dermatology & Burn Care")

        fracture = ClinicalHeuristicClassifier.classify({"redness_index": 3.0, "edge_density": 12.0}, clinical_hint="fracture")
        self.assertIn("Fracture", fracture["injury_type"])
        self.assertEqual(fracture["recommended_specialty"], "Orthopedic Surgery")

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_receptionist.db")
        self.db = DatabaseManager(db_path=self.db_path)
        self.db.initialize_schema()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_database_initialization(self):
        doctors = self.db.fetch_all_doctors()
        self.assertEqual(len(doctors), 7)
        trauma_docs = [d for d in doctors if d["specialty"] == "Trauma & Emergency"]
        self.assertTrue(len(trauma_docs) >= 1)

    def test_specialist_search(self):
        burn_docs = self.db.find_specialists("Burn Care")
        self.assertTrue(len(burn_docs) >= 1)
        self.assertIn("Burn", burn_docs[0]["specialty"])

    def test_triage_logging_and_assignment(self):
        triage_id, ticket_num = self.db.record_triage(
            injury_type="Deep Dermal Laceration",
            severity="Urgent",
            confidence=0.95,
            specialty_needed="Trauma & Emergency",
            first_aid="Apply continuous direct pressure | Sterile dressing",
            doctor_id=None
        )
        self.assertGreater(triage_id, 0)
        self.assertTrue(ticket_num.startswith("ER-"))

        # Dispatch doctor
        doctors = self.db.fetch_all_doctors()
        assignment = self.db.assign_doctor(triage_id, doctors[0]["id"])
        self.assertEqual(assignment["ticket_num"], ticket_num)
        self.assertEqual(assignment["doctor"]["id"], doctors[0]["id"])

        # History audit
        history = self.db.fetch_recent_scans(limit=5)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["patient_ticket"], ticket_num)

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_probe(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "HEALTHY")
        self.assertTrue(data["database_connected"])

    def test_doctors_list(self):
        resp = self.client.get("/api/doctors")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 7)

    def test_scan_and_dispatch_flow(self):
        with open("static/samples/laceration.jpg", "rb") as f:
            b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

        scan_resp = self.client.post("/api/scan", json={
            "image_base64": b64,
            "hint_type": "laceration"
        })
        self.assertEqual(scan_resp.status_code, 200)
        data = scan_resp.json()
        self.assertEqual(data["injury_type"], "Deep Dermal Laceration")
        self.assertTrue(len(data["recommended_doctors"]) >= 1)

        # Dispatch doctor
        doc_id = data["recommended_doctors"][0]["id"]
        assign_resp = self.client.post("/api/assign", json={
            "triage_id": data["triage_id"],
            "doctor_id": doc_id
        })
        self.assertEqual(assign_resp.status_code, 200)
        self.assertEqual(assign_resp.json()["status"], "success")

    def test_malformed_input_rejection(self):
        resp = self.client.post("/api/scan", json={"image_base64": "invalid_truncated_string"})
        self.assertIn(resp.status_code, [400, 422])

if __name__ == "__main__":
    unittest.main(verbosity=2)
