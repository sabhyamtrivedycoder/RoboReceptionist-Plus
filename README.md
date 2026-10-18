# Robo Receptionist + 🚑🤖
> **Late-Night Emergency Hospital Triage System**  
> *Built with Computer Vision (OpenCV), Multimodal Vision AI, and SQL Doctor Dispatch Architecture*

---

## 📌 Executive Summary
**Robo Receptionist +** is an autonomous emergency hospital triage station engineered to solve late-night hospital congestion and triage delays. Patients presenting with physical trauma (lacerations, fractures, burns, ocular trauma, contusions) are optically scanned via live camera or upload. 

The system leverages a dual-tier vision pipeline:
1. **OpenCV 5.0 Edge & Erythema Optical Telemetry**: Performs real-time tissue damage segmentation using HSV erythema thresholding, Canny edge gradient analysis, and contour localization with tactical HUD bounding boxes.
2. **Multimodal Vision Intelligence (Google Gemini 1.5 Flash / OpenAI GPT-4o-mini)**: Performs clinical-grade injury classification, severity stratification (Emergency / Urgent / Moderate), and emergency first-aid instruction generation.
3. **SQLite Doctor Dispatch Engine**: Real-time relational database querying on-call specialists by specialty, sub-specialty, experience, and duty status to immediately alert and dispatch the appropriate medical team.

---

## ⚙️ Key Technical Features
* **Zero-Failure Offline Heuristics**: If no API key is provided or the network is unavailable, an OpenCV heuristic engine dynamically calculates redness ratios and edge gradients to classify injuries deterministically.
* **Cyberpunk Medical Tactical HUD**: Emerald green (`#00ff66`) on obsidian black interface with live scanning radar, visual crosshairs, confidence meters, and audio-visual alerts.
* **Pre-Seeded Specialist Directory**: 7 medical specialists across Trauma Surgery, Orthopedics, Plastic Surgery, Burn Care, Ophthalmology, Neurology, and General ER.
* **Persistent SQLite Audit Trail**: Stores all scan telemetry, patient ticket numbers, severity grades, and doctor dispatch logs.

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.10+ (Python 3.12 verified)
- Web browser (Chrome, Edge, Firefox, Brave)
- Webcam (optional, file upload & sample cases included)

### 2. One-Click Launch (Windows)
Double-click:
```bat
run_website.bat
```
The terminal will start the server and automatically launch `http://localhost:5000` in your browser.

### 3. Manual Launch
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```
Visit: **[http://localhost:5000](http://localhost:5000)**

---

## 🩺 Supervisor Demonstration Walkthrough
When demonstrating to your supervisor, use these 3 steps:

1. **Test Pre-Loaded Sample Cases**:
   - Click the **"🧪 Samples"** tab.
   - Click **"Deep Laceration"** &rarr; Hit **"INITIALIZE CV SCAN & MATCH DOCTOR"**.
   - Watch the radar scan, contour detection bounding box, redness index calculation, and instant assignment of **Dr. Vikram Sen (Chief of Trauma Surgery)**.
   - Click **"DISPATCH"** to see the emergency alert ticket generated.

2. **Test Live Camera / File Upload**:
   - Switch to **"📁 File Upload"** or **"📷 Camera"**.
   - Point your camera at a test image or upload any wound photo.
   - The OpenCV engine localizes the region of interest and extracts tissue metrics.

3. **Show SQLite Doctor Registry**:
   - Scroll down to the **"Real-Time ER Triage Logs"** table.
   - Show how tickets (`ER-XXXXXX`), timestamps, severity, and assigned doctors persist in `receptionist.db`.

---

## 🏗️ Project Architecture
```
RoboReceptionist-Plus/
├── app.py                   # FastAPI backend server & REST API
├── cv_engine.py             # OpenCV image processing & Multimodal AI pipeline
├── database.py              # SQLite relational schema, seed data & queries
├── receptionist.db          # Active SQLite database file
├── run_website.bat          # 1-click Windows batch launcher
├── requirements.txt         # Python dependencies
├── static/
│   └── samples/             # 5 pre-loaded clinical sample cases
└── templates/
    └── index.html           # Dark-mode cyberpunk frontend UI
```
