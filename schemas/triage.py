"""
schemas/triage.py - Clinical Triage Input & Output Schemas
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from schemas.doctor import DoctorRead

class TriageSeverity(str, Enum):
    EMERGENCY = "Emergency"
    URGENT = "Urgent"
    MODERATE = "Moderate"
    MILD = "Mild"

class BoundingBox(BaseModel):
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)

class OpticalTelemetryMetrics(BaseModel):
    redness_index: float = Field(..., ge=0.0, le=100.0, description="Erythema and extravasation ratio in %")
    edge_density: float = Field(..., ge=0.0, le=100.0, description="Canny edge structural boundary density in %")
    lesion_surface_area_ratio: float = Field(default=0.0, description="Estimated lesion surface footprint ratio")
    bbox: Optional[BoundingBox] = None

class ScanRequestPayload(BaseModel):
    image_base64: str = Field(..., min_length=50, description="Raw base64 encoded image or Data URL")
    api_key: Optional[str] = Field(default="", description="Optional upstream LLM vision key")
    provider: Optional[str] = Field(default="auto", description="Provider selector: 'auto', 'gemini', or 'openai'")
    hint_type: Optional[str] = Field(default=None, description="Optional clinical test case identifier")

    @field_validator("image_base64")
    @classmethod
    def validate_image_payload(cls, value: str) -> str:
        if not value or len(value.strip()) < 50:
            raise ValueError("Payload contains an empty or truncated image binary.")
        return value.strip()

class TriageTicketResponse(BaseModel):
    triage_id: int
    patient_ticket: str
    injury_type: str
    severity: TriageSeverity
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: str
    recommended_specialty: str
    first_aid: List[str]
    ai_source: str
    opencv_metrics: OpticalTelemetryMetrics
    annotated_image: str
    recommended_doctors: List[DoctorRead]

class DoctorAssignmentRequest(BaseModel):
    triage_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)

class AssignmentResponse(BaseModel):
    status: str = "success"
    triage_id: int
    ticket_num: str
    doctor: Optional[DoctorRead]
