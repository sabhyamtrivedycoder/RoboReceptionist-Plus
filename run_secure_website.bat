@echo off
TITLE Robo Receptionist + // Secure HTTPS Medical Triage
COLOR 0A

echo =======================================================================
echo     ROBO RECEPTIONIST +  //  SECURE HTTPS EMERGENCY TRIAGE SYSTEM
echo =======================================================================
echo.
echo [1/3] Verifying Python Environment...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in system PATH.
    pause
    exit /b 1
)

echo [2/3] Verifying SSL/TLS Certificates...
if not exist "cert.pem" (
    echo Generating local SSL certificate (cert.pem, key.pem)...
    python generate_cert.py
)

echo [3/3] Launching Secure HTTPS Web Server on Port 5000...
echo.
echo =======================================================================
echo   SECURE HTTPS ONLINE: https://localhost:5000
echo   Alternative Address: https://127.0.0.1:5000
echo =======================================================================
echo.
echo * If your browser asks to confirm the local development certificate:
echo   Click "Advanced" -^> "Proceed to localhost (continue)" to open.
echo.

REM Open browser to secure HTTPS endpoint after 2 seconds
start /b cmd /c "timeout /t 2 /nobreak >nul && start https://localhost:5000"

REM Run Uvicorn with SSL encryption
python -m uvicorn app:app --host 127.0.0.1 --port 5000 --ssl-keyfile key.pem --ssl-certfile cert.pem

pause
