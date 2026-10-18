@echo off
TITLE Robo Receptionist + // Emergency Triage System
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
    echo Please install Python 3.10+ or check your environment variables.
    pause
    exit /b 1
)

echo [2/3] Checking SQLite Database and Model Assets...
if not exist "receptionist.db" (
    echo Initializing database schema and seeding emergency specialists...
    python -c "import database; database.init_db()"
)

echo [3/3] Launching Web Application on Port 5000...
echo.
echo =======================================================================
echo  Terminal HUD Online: http://localhost:5000
echo  Press CTRL + C to stop the server anytime.
echo =======================================================================
echo.

REM Open browser automatically after 2 seconds
start /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5000"

REM Run Uvicorn ASGI Web Server
python -m uvicorn app:app --host 0.0.0.0 --port 5000

pause
