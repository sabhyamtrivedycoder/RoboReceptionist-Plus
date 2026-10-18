@echo off
TITLE Push Robo Receptionist + to GitHub
COLOR 0B

echo =======================================================================
echo          ROBO RECEPTIONIST +  //  GITHUB HOSTING LAUNCHER
echo =======================================================================
echo.
echo This script will connect your local repository to GitHub and push your code.
echo.
echo STEP 1: Go to https://github.com/new
echo STEP 2: Name your repository (e.g., RoboReceptionist-Plus)
echo STEP 3: Keep it Public, DO NOT check "Add a README" or ".gitignore"
echo STEP 4: Click "Create repository"
echo.
echo =======================================================================
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/username/RoboReceptionist-Plus.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No repository URL provided. Aborting.
    pause
    exit /b 1
)

echo.
echo [1/3] Setting git remote origin...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%

echo [2/3] Verifying branch name (main)...
git branch -M main

echo [3/3] Pushing code to GitHub...
echo (If prompted, sign in via your browser or Personal Access Token)
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================================
    echo [SUCCESS] Code pushed to GitHub successfully!
    echo.
    echo To view your live hosted website on GitHub Pages:
    echo 1. Go to your repository on GitHub
    echo 2. Click Settings -^> Pages
    echo 3. Under "Build and deployment", choose:
    echo    - Source: GitHub Actions (Recommended) OR Deploy from a branch (main)
    echo 4. Your site will be live at: https://<username>.github.io/<repo-name>/
    echo =======================================================================
) else (
    echo.
    echo [NOTE] Push returned an error. Please verify your GitHub URL and permissions.
)

pause
