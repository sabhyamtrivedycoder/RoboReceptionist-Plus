# Robo Receptionist +
> **Emergency Department Clinical Triage & Specialist Referral System**  
> *Built with Optical Computer Vision, Emergency Severity Index (ESI v4) Classification, and Relational On-Call Dispatch*

---

## 1. System Overview
Robo Receptionist + is an autonomous clinical triage workstation engineered for acute emergency departments and trauma centers. The system assesses patients presenting with physical injury (lacerations, thermal burns, musculoskeletal trauma, ocular trauma, contusions) via calibrated optical ingestion.

The architecture comprises three core systems:
1. **Optical Diagnostic Ingestion**: Real-time pixel-level tissue segmentation utilizing HSV colorimetry (erythema and necrosis extraction), Sobel edge gradient convolution, and connected contour bounding box isolation.
2. **Clinical Decision Tree (ESI v4 & Manchester Triage System)**: Classifies patient presentation into Emergency Severity Index acuity grades (ESI Levels 1 through 5), generating ICD-10 diagnostic classifications, estimated hemodynamic profiles (Heart Rate, Blood Pressure, SpO2, GCS, RTS), and immediate stabilization procedures.
3. **Specialist Referral Registry**: Queries relational and on-duty physician directories to match patients to on-call surgeons, emergency physicians, and burn reconstructive specialists.

---

## 2. Technical Capabilities
* **In-Browser & Server Dual Pipeline**: Operates both via FastAPI server or fully client-side in static browser environments (WebAssembly / Canvas).
* **Objective Tissue Metrics**: Calculates quantitative metrics including Erythema Index (%), Edge Gradient Energy (%), Lesion Surface Footprint (%), and Devitalized Tissue Ratio (%).
* **FHIR / HL7 Admission Profile Export**: Exports standardized ClinicalImpression JSON records containing vital telemetry, ICD-10 codes, and stabilization steps.
* **Audit Registry**: Tracks all patient encounters, timestamps, triage acuity grades, and attending physician assignments in SQLite with Write-Ahead Logging (WAL).

---

## 3. Quick Start Guide

### Requirements
- Python 3.10+ (Verified on Python 3.12)
- Modern Web Browser (Chrome, Edge, Firefox, Safari)
- Camera input or local image files

### Launch via Batch File (Windows)
```bat
run_website.bat
```
This initializes the backend server and opens the clinical console at `http://localhost:5000`.

### Manual Launch via Command Line
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated test suite
python run_tests.py

# 3. Launch application server
python app.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 4. Project Structure
```
RoboReceptionist-Plus/
├── app.py                      # FastAPI application with latency middleware and RFC 7807 handlers
├── cv_engine.py                # 4-tier OpenCV optical segmentation & heuristic inference
├── database.py                 # Thread-safe DatabaseManager with SQLite WAL journaling
├── run_tests.py                # Automated unit and integration test suite
├── index.html                  # Clinical emergency department console (GitHub Pages compatible)
├── static/
│   ├── js/
│   │   ├── vision_core.js      # Pixel-level HSV, Sobel, and contour bounding box engine
│   │   ├── triage_classifier.js# ESI v4 emergency decision matrix & ICD-10 mappings
│   │   ├── specialists_roster.js# Hospital directory of on-call specialist physicians
│   │   └── app_controller.js   # Application coordinator & state machine
│   └── samples/                # Authenticated clinical test cases
└── templates/
    └── index.html              # Server-rendered template mirror
```

---

## 5. Verification & Testing
Run the automated test suite:
```bash
python run_tests.py
```
All 11 integration and unit tests verify:
- Database schema initialization, foreign keys, and WAL pragma configuration
- Specialist queries and on-call status filtering
- Triage ticket logging and physician assignment
- Optical pipeline base64 decoding, Canny gradient calculation, and HSV thresholding
- FastAPI REST endpoints (`/health`, `/api/doctors`, `/api/scan`, `/api/assign`, `/api/analytics`)
