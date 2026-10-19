# Robo Receptionist +

<div align="center">
  <img src="static/img/logo_full.svg" alt="Robo Receptionist + Logo" width="480">
  <br>
  <p><strong>Open-Source Autonomous Clinical Triage &amp; Emergency Specialist Referral System</strong></p>
  <p><em>Deterministic Optical Computer Vision &middot; Emergency Severity Index (ESI v4) &middot; Relational Specialist Dispatch</em></p>

  <p>
    <a href="https://github.com/sabhyamtrivedycoder/RoboReceptionist-Plus/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-10b981.svg" alt="License: MIT"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10%2B-06b6d4.svg" alt="Python 3.10+"></a>
    <img src="https://img.shields.io/badge/Tests-11%2F11%20Passing-22c55e.svg" alt="Tests 11/11 Passing">
    <img src="https://img.shields.io/badge/Clinical%20Protocol-ESI%20v4-f59e0b.svg" alt="Clinical Protocol: ESI v4">
    <img src="https://img.shields.io/badge/Emojis-Strictly%20Zero-8b5cf6.svg" alt="Emojis: Strictly Zero">
    <a href="https://sabhyamtrivedycoder.github.io/RoboReceptionist-Plus/"><img src="https://img.shields.io/badge/Demo-GitHub%20Pages-10b981.svg" alt="Demo: GitHub Pages"></a>
  </p>
</div>

---

## 1. System Overview
Robo Receptionist + is an autonomous clinical emergency workstation engineered for acute emergency departments and trauma centers. The workstation assesses patients presenting with physical trauma (lacerations, thermal burns, musculoskeletal trauma, ocular injury, acute contusions) via calibrated optical ingestion.

The architecture comprises three core systems:
1. **Optical Diagnostic Ingestion**: Real-time pixel-level tissue segmentation utilizing HSV colorimetry (erythema and necrosis extraction), Sobel edge gradient convolution, and connected contour bounding box isolation.
2. **Clinical Decision Tree (ESI v4 & Manchester Triage System)**: Classifies patient presentation into Emergency Severity Index acuity grades (ESI Levels 1 through 5), generating ICD-10 diagnostic classifications, estimated hemodynamic profiles (Heart Rate, Blood Pressure, SpO2, GCS, RTS), and immediate stabilization procedures.
3. **Specialist Referral Registry**: Queries relational and on-duty physician directories to match patients to on-call surgeons, emergency physicians, and burn reconstructive specialists.

---

## 2. Technical Capabilities
* **100% Open Source (MIT License)**: Free, auditable, and extensible clinical informatics software.
* **Green &amp; Black Clinical Health-Tech Aesthetic**: Obsidian carbon background (`#040806`), luminous emerald identity (`#10b981`), and high-contrast clinical telemetry colors (cyan, amber, acute red, and purple).
* **Dual Runtime Pipeline**: Operates both via FastAPI server or fully client-side in static browser environments (WebAssembly / Canvas).
* **Objective Tissue Metrics**: Calculates quantitative metrics including Erythema Index (%), Edge Gradient Energy (%), Lesion Surface Footprint (%), and Devitalized Tissue Ratio (%).
* **FHIR / HL7 Admission Profile Export**: Exports standardized ClinicalImpression JSON records containing vital telemetry, ICD-10 codes, and stabilization steps.
* **Audit Registry**: Tracks all patient encounters, timestamps, triage acuity grades, and attending physician assignments in SQLite with Write-Ahead Logging (WAL).
* **Zero-Emoji Enforcement**: Medical-grade communication standards across all code, documentation, and user interfaces.

---

## 3. Quick Start Guide

### Requirements
- Python 3.10+ (Verified on Python 3.10, 3.11, 3.12)
- Modern Web Browser (Chrome, Edge, Firefox, Safari)
- Camera input or local clinical image files

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
- **Home (`index.html`)**: Editorial explanation, central animated workstation simulation, live ECG cardiac pulse rhythm, "Try Robo Receptionist" primary CTA, and centered LinkedIn connect section.
- **Triage Console (`triage.html`)**: Interactive clinical diagnostic workstation (optical webcam stream, image upload, 3x3 Sobel convolution, ESI acuity grading, on-call doctor paging, FHIR export, and audit registry).
- **About (`about.html`)**: Clinical emergency mission, the nocturnal ER intake crisis, why deterministic optical CV beats generative black boxes, and engineering principles.
- **Latest Work (`latest-work.html`)**: In-depth scientific methodology, HSV colorimetric formula, 3x3 Sobel kernels, ESI v4 decision matrices, and Triage-Bench accuracy benchmarks.
- **Contact (`contact.html`)**: Dedicated institutional inquiry and collaboration page featuring the verified LinkedIn redirect button.

```
RoboReceptionist-Plus/
├── LICENSE                     # Permissive MIT Open Source License
├── CONTRIBUTING.md              # Contributor guidelines and testing protocols
├── CODE_OF_CONDUCT.md           # Contributor Covenant Code of Conduct
├── README.md                   # Project documentation and specifications
├── app.py                      # FastAPI application with latency middleware and RFC 7807 handlers
├── cv_engine.py                # 4-tier OpenCV optical segmentation & heuristic inference
├── database.py                 # Thread-safe DatabaseManager with SQLite WAL journaling
├── run_tests.py                # Automated unit and integration test suite (11/11 passing)
├── index.html                  # Homepage with optical simulation & Try Robo Receptionist CTA
├── triage.html                 # Dedicated interactive diagnostic terminal workstation
├── about.html                  # Mission, clinical emergency problem, and architecture
├── latest-work.html            # HSV colorimetry, Sobel kernels, and ESI v4 methodology
├── contact.html                # Dedicated contact page with LinkedIn redirect
├── templates/                  # Server-rendered template mirror for FastAPI
├── static/
│   ├── favicon.svg             # High-resolution clinical vector favicon
│   ├── img/
│   │   ├── logo_mark.svg       # Vector medical cross & optical reticle emblem
│   │   └── logo_full.svg       # Full horizontal vector branding logo
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

---

## 6. Open Source Governance
* **License**: Released under the [MIT License](LICENSE).
* **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for pull request guidelines, commit formatting, and testing rules.
* **Code of Conduct**: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.
* **Professional Contact**: Connect via [LinkedIn](https://www.linkedin.com/in/riddhiman-gupta-4075b1396/).
