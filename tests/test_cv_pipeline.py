"""
tests/test_cv_pipeline.py - Unit Tests for Optical Feature Extractor & Heuristics
"""

import pytest
import numpy as np
import cv2
import base64

from cv_engine import OpticalFeatureExtractor, ClinicalHeuristicClassifier
from core.exceptions import ImageDecodingError

@pytest.fixture
def feature_extractor():
    return OpticalFeatureExtractor()

@pytest.fixture
def sample_synthetic_wound_image():
    """Generates an in-memory 240x240 image with a distinct red/inflamed locus."""
    img = np.ones((240, 240, 3), dtype=np.uint8) * 190  # skin-like tone
    # Inject red lesion
    cv2.circle(img, (120, 120), 45, (20, 20, 230), -1)
    cv2.line(img, (90, 120), (150, 120), (10, 10, 140), 3)
    return img

def test_base64_encode_decode_roundtrip(feature_extractor, sample_synthetic_wound_image):
    b64 = feature_extractor.encode_cv2_to_base64(sample_synthetic_wound_image)
    assert b64.startswith("data:image/jpeg;base64,")

    decoded = feature_extractor.decode_base64_to_cv2(b64)
    assert decoded.shape == sample_synthetic_wound_image.shape
    assert decoded.dtype == np.uint8

def test_malformed_base64_rejection(feature_extractor):
    with pytest.raises(ImageDecodingError):
        feature_extractor.decode_base64_to_cv2("not_a_valid_base64_payload")

def test_optical_telemetry_extraction(feature_extractor, sample_synthetic_wound_image):
    telemetry = feature_extractor.extract_telemetry(sample_synthetic_wound_image)
    assert "redness_index" in telemetry
    assert "edge_density" in telemetry
    assert "annotated_image" in telemetry
    assert "bbox" in telemetry

    # Verify redness index is positive for a synthetic red lesion
    assert telemetry["redness_index"] > 5.0
    assert telemetry["bbox"] is not None
    assert telemetry["bbox"]["width"] > 0

def test_deterministic_burn_heuristic_classification():
    mock_metrics = {"redness_index": 24.5, "edge_density": 4.1}
    diagnosis = ClinicalHeuristicClassifier.classify(mock_metrics, clinical_hint=None)
    assert diagnosis["injury_type"] == "Second-Degree Thermal Burn"
    assert diagnosis["recommended_specialty"] == "Dermatology & Burn Care"

def test_deterministic_fracture_heuristic_classification():
    mock_metrics = {"redness_index": 4.2, "edge_density": 11.8}
    diagnosis = ClinicalHeuristicClassifier.classify(mock_metrics, clinical_hint="fracture")
    assert "Fracture" in diagnosis["injury_type"]
    assert diagnosis["recommended_specialty"] == "Orthopedic Surgery"
