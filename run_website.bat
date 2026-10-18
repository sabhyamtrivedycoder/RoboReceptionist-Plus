@echo off
TITLE Robo Receptionist + // Launcher
COLOR 0A

echo =======================================================================
echo          ROBO RECEPTIONIST + // AI EMERGENCY HOSPITAL TRIAGE
echo       Computer Vision Injury Detection & Specialist Doctor Dispatch
echo =======================================================================
echo.
echo [1/3] Verifying Python Environment...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in system PATH.
    pause
    exit /b 1
)

echo [2/3] Checking SQLite Database and SSL Certificates...
if not exist "receptionist.db" (
    python -c "import database; database.init_db()"
)

if not exist "cert.pem" (
    python generate_cert.py
)

echo [3/3] Launching Secure HTTPS Web Server on Port 5000...
echo.
echo =======================================================================
echo  Secure HTTPS Terminal: https://localhost:5000
echo  Alternative Address:   https://127.0.0.1:5000
echo =======================================================================
echo.

REM Automatically open default browser after 2 seconds
start /b cmd /c "timeout /t 2 /nobreak >nul && start https://localhost:5000"

REM Launch Uvicorn with SSL encryption
python -m uvicorn app:app --host 127.0.0.1 --port 5000 --ssl-keyfile key.pem --ssl-certfile cert.pem

pause
