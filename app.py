"""
app.py - Main FastAPI Server for Robo Receptionist +
Late-Night Emergency Triage, Computer Vision Injury Analysis & Specialist Doctor Assignment
"""

import os
import json
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import database
import cv_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and seed on startup
    database.init_db()
    print("[Robo Receptionist +] Database initialized with emergency specialists on call.")
    yield

app = FastAPI(
    title="Robo Receptionist +",
    description="Emergency Triage & Specialist Doctor Recommendation System using OpenCV & Multimodal Vision",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for maximum flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files & Templates
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Request Models
class ScanRequest(BaseModel):
    image_base64: str
    api_key: Optional[str] = ""
    provider: Optional[str] = "auto"
    hint_type: Optional[str] = None

class AssignRequest(BaseModel):
    triage_id: int
    doctor_id: int

# Routes
@app.get("/")
async def serve_index(request: Request):
    """Renders the main Robo Receptionist + triage dashboard."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "online",
        "system": "Robo Receptionist +",
        "opencv_version": cv_engine.cv2.__version__,
        "database": "SQLite (Active)"
    }

@app.get("/api/doctors")
async def get_all_doctors():
    """Returns the list of on-call emergency medical specialists."""
    return database.get_all_doctors()

@app.get("/api/history")
async def get_history():
    """Returns the latest triage logs from the SQLite database."""
    return database.get_recent_scans(limit=15)

@app.post("/api/scan")
async def scan_injury(req: ScanRequest):
    """
    Core CV & AI Triage Pipeline:
    1. Runs OpenCV optical telemetry (redness ratio, edge gradient, ROI bounding box).
    2. Runs Multimodal Vision AI (Gemini / OpenAI) if API key provided.
    3. Deterministically falls back to OpenCV heuristic engine if offline/unconfigured.
    4. Queries SQLite for specialists matching the injury diagnosis.
    5. Saves the triage ticket to SQLite database.
    """
    if not req.image_base64:
        raise HTTPException(status_code=400, detail="Missing image data")

    try:
        # Run CV analysis and AI triage
        triage_res = await cv_engine.run_injury_triage(
            image_b64=req.image_base64,
            api_key=req.api_key or "",
            provider=req.provider or "auto",
            hint_type=req.hint_type
        )

        # Query matching on-call specialists from SQLite
        recommended_specialty = triage_res.get("recommended_specialty", "General Emergency Medicine")
        matched_doctors = database.find_doctors_for_specialty(recommended_specialty)

        # Log triage ticket into SQLite
        first_aid_str = " | ".join(triage_res.get("first_aid", []))
        triage_id, ticket_num = database.log_triage(
            injury_type=triage_res.get("injury_type", "Acute Trauma"),
            severity=triage_res.get("severity", "Urgent"),
            confidence=float(triage_res.get("confidence", 0.9)),
            specialty_needed=recommended_specialty,
            first_aid=first_aid_str,
            doctor_id=None,
            image_preview=""
        )

        return {
            "triage_id": triage_id,
            "patient_ticket": ticket_num,
            "injury_type": triage_res.get("injury_type"),
            "severity": triage_res.get("severity"),
            "confidence": triage_res.get("confidence"),
            "description": triage_res.get("description"),
            "recommended_specialty": recommended_specialty,
            "first_aid": triage_res.get("first_aid", []),
            "ai_source": triage_res.get("ai_source"),
            "opencv_metrics": triage_res.get("opencv_metrics"),
            "annotated_image": triage_res.get("annotated_image"),
            "recommended_doctors": matched_doctors
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Triage pipeline failed: {str(e)}")

@app.post("/api/assign")
async def assign_doctor(req: AssignRequest):
    """Assigns an emergency medical specialist to a triage ticket and alerts the department."""
    try:
        result = database.assign_doctor_to_triage(req.triage_id, req.doctor_id)
        return {
            "status": "success",
            "triage_id": req.triage_id,
            "ticket_num": result.get("ticket_num"),
            "doctor": result.get("doctor")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Doctor assignment failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 65)
    print("  ROBO RECEPTIONIST +  //  EMERGENCY TRIAGE INTELLIGENCE")
    print("  Server running at: http://localhost:5000")
    print("=" * 65 + "\n")
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
