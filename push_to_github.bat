@echo off
setlocal enabledelayedexpansion

echo =====================================================================
echo  SENTINEL-X 1A: Push to GitHub Repository for Srujan-Joshi
echo =====================================================================
echo.

where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git is not detected in your system PATH.
    echo.
    echo Please install Git for Windows from:
    echo https://git-scm.com/download/win
    echo.
    echo Or install GitHub Desktop from:
    echo https://desktop.github.com/
    echo.
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
git init

echo [2/5] Staging all files...
git add .

echo [3/5] Creating commit...
git commit -m "feat: complete frontend, backend, and open benchmarks for SENTINEL-X 1A"

echo [4/5] Setting default branch to main...
git branch -M main

set REPO_NAME=sentinel-x-threat-fusion
echo.
echo Remote target repository: https://github.com/Srujan-Joshi/%REPO_NAME%.git
echo Make sure you have created this repository on GitHub under Srujan-Joshi:
echo https://github.com/new?name=%REPO_NAME%
echo.

git remote remove origin 2>nul
git remote add origin https://github.com/Srujan-Joshi/%REPO_NAME%.git

echo [5/5] Pushing code to GitHub...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo =====================================================================
    echo [SUCCESS] Code pushed successfully to:
    echo https://github.com/Srujan-Joshi/%REPO_NAME%
    echo =====================================================================
) else (
    echo.
    echo [NOTE] If the push failed, verify:
    echo 1. You created the repository on https://github.com/new?name=%REPO_NAME%
    echo 2. You are logged into GitHub in your terminal / browser
)

pause
