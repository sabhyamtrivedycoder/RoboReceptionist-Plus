"""
schemas/doctor.py - Doctor Entity Validation Schemas
"""

from pydantic import BaseModel, Field

class DoctorBase(BaseModel):
    name: str = Field(..., example="Dr. Vikram Sen")
    title: str = Field(..., example="Chief of Trauma Surgery")
    specialty: str = Field(..., example="Trauma & Emergency")
    sub_specialty: str = Field(..., example="Acute Trauma, Hemorrhage Control")
    department: str = Field(..., example="Emergency Department (Red Bay)")
    experience_years: int = Field(..., ge=1, le=50)
    rating: float = Field(..., ge=1.0, le=5.0)
    on_call_night: bool = True
    phone: str = Field(..., example="+91 98112-40912")
    email: str = Field(..., example="v.sen@cityhospital.org")
    avatar_url: str
    status: str = Field(default="Available")
    room_number: str = Field(..., example="ER-Trauma-01")

class DoctorRead(DoctorBase):
    id: int

    class Config:
        from_attributes = True
