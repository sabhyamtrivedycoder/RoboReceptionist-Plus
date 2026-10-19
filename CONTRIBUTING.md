# Contributing to Robo Receptionist +

Thank you for your interest in contributing to Robo Receptionist +, an open-source autonomous clinical triage and specialist referral platform.

Our mission is to eliminate nocturnal emergency room intake bottlenecks through reproducible optical computer vision, standardized Emergency Severity Index (ESI v4) decision matrices, and deterministic diagnostic algorithms.

---

## 1. Guiding Principles & Non-Negotiable Standards

Before contributing code, please note these fundamental engineering tenets:

1. **Strict Zero-Emoji Policy**:
   - Emojis are strictly forbidden across the entire codebase, including HTML templates, JavaScript controllers, Python modules, CSS, commit messages, and documentation.
   - Emergency medical informatics demands sober, board-certified clinical rigor and professional typography.

2. **Deterministic Verification over Black-Box Hallucinations**:
   - The primary triage classification engine must execute deterministically using calibrated optical filters (HSV colorimetry, 3x3 Sobel spatial gradient convolution) and mathematically bounded ESI decision trees.
   - External LLMs or multimodal foundation models may only serve as advisory or fallback providers, never as unverified primary arbiters of acute trauma.

3. **Sub-Second Performance**:
   - Local triage inference must complete in under 850 milliseconds.
   - Client-side static fallback pipelines must function in complete offline isolation.

4. **100% Test Coverage & Zero Regressions**:
   - All proposed modifications must pass the complete automated test suite (`python run_tests.py`) with zero failures or skipped assertions.

---

## 2. Development Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git
- Modern web browser (Chrome, Edge, Firefox, Safari)

### Local Environment Setup
```bash
# 1. Clone the repository
git clone https://github.com/sabhyamtrivedycoder/RoboReceptionist-Plus.git
cd RoboReceptionist-Plus

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify test suite
python run_tests.py

# 5. Launch development server
python app.py
```
Access the local diagnostic workstation at `http://127.0.0.1:5000`.

---

## 3. Repository Architecture

```
RoboReceptionist-Plus/
├── app.py                      # FastAPI ASGI application with RFC 7807 error boundaries
├── cv_engine.py                # 4-tier OpenCV optical segmentation & heuristic inference
├── database.py                 # Thread-safe DatabaseManager with SQLite WAL journaling
├── run_tests.py                # Automated unit and integration test suite
├── index.html                  # Editorial homepage with 3D device simulation
├── triage.html                 # Interactive clinical diagnostic terminal workstation
├── about.html                  # Architectural tenets & the 3:00 AM clinical crisis
├── latest-work.html            # Triage-Bench clinical benchmark publication
├── contact.html                # Institutional inquiries & verified contact card
├── templates/                  # Server-rendered Jinja2 template mirror
├── static/
│   ├── js/
│   │   ├── vision_core.js      # Pixel-level HSV, Sobel, and contour bounding box engine
│   │   ├── triage_classifier.js# ESI v4 emergency decision matrix & ICD-10 mappings
│   │   ├── specialists_roster.js# Hospital directory of on-call specialist physicians
│   │   └── app_controller.js   # Application coordinator & state machine
│   ├── img/
│   │   ├── logo_mark.svg       # Vector medical-AI aperture emblem
│   │   └── logo_full.svg       # Full editorial logo with typography
│   └── samples/                # Authenticated clinical test cases
```

---

## 4. Submitting Pull Requests

1. **Create a Topic Branch**:
   ```bash
   git checkout -b feature/optical-enhancement
   ```

2. **Commit Message Format**:
   Follow Conventional Commits without emojis:
   - `feat: add bilateral spatial filter to pre-triage pipeline`
   - `fix: resolve bounding box coordinate clamping on mobile viewports`
   - `docs: update Triage-Bench methodology citation`
   - `test: add unit test for necrotic tissue edge detection`

3. **Verify Locally**:
   ```bash
   python run_tests.py
   ```

4. **Submit PR**:
   - Open a pull request against `main`.
   - Provide clinical justification, execution benchmarks, and evidence that all 11 tests pass.

---

## 5. Licensing

By contributing to Robo Receptionist +, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
