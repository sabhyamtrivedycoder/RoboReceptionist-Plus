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

## 4. Multi-Page Architecture & Project Structure
Robo Receptionist + is structured into dedicated, modular pages:
- **Home (`index.html`)**: Editorial explanation, central animated AI demonstration showcase with floating telemetry cards, "Try Robo Receptionist" primary CTA, and "Get in touch" LinkedIn section.
- **Triage Console (`triage.html`)**: Full interactive diagnostic workstation (webcam stream, upload, 3x3 Sobel convolution, ESI acuity grading, on-call doctor paging, FHIR export, and audit registry).
- **About (`about.html`)**: Clinical emergency mission, the late-night ER intake crisis, why deterministic optical CV beats generative black boxes, and engineering principles.
- **Latest Work (`latest-work.html`)**: In-depth scientific methodology, HSV colorimetric formula, 3x3 Sobel kernels, ESI v4 decision matrices, and HL7/FHIR export protocols.
- **Contact (`contact.html`)**: Dedicated "Get in touch" page featuring the verified LinkedIn redirect button.

```
RoboReceptionist-Plus/
├── app.py                      # FastAPI application with latency middleware and RFC 7807 handlers
├── cv_engine.py                # 4-tier OpenCV optical segmentation & heuristic inference
├── database.py                 # Thread-safe DatabaseManager with SQLite WAL journaling
├── run_tests.py                # Automated unit and integration test suite
├── index.html                  # Homepage with central video demonstration & Try Robo Receptionist CTA
├── triage.html                 # Dedicated interactive diagnostic terminal workstation
├── about.html                  # Mission, clinical emergency problem, and architecture
├── latest-work.html            # HSV colorimetry, Sobel kernels, and ESI v4 methodology
├── contact.html                # Dedicated contact page with LinkedIn redirect
├── templates/                  # Server-rendered template mirror for FastAPI
├── static/
│   ├── js/
│   │   ├── vision_core.js      # Pixel-level HSV, Sobel, and contour bounding box engine
│   │   ├── triage_classifier.js# ESI v4 emergency decision matrix & ICD-10 mappings
│   │   ├── specialists_roster.js# Hospital directory of on-call specialist physicians
│   │   └── app_controller.js   # Application coordinator & state machine
│   └── samples/                # Authenticated clinical test cases
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
