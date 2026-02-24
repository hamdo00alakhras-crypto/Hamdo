@echo off
chcp 65001 >nul
title Hamdo - Jewelry E-commerce Platform

echo ========================================
echo    Hamdo - Jewelry E-commerce Platform
echo ========================================
echo.

echo [1/3] Checking MySQL...
sc query MySQL >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] MySQL service not found. 
    echo     Please start XAMPP and run MySQL service.
) else (
    echo [OK] MySQL service found
)

echo.
echo [2/3] Starting Backend Server (FastAPI)...
start "Hamdo Backend - FastAPI Server" cmd /k "cd /d G:\Hamdo && venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"
echo [OK] Backend starting on http://localhost:8000

echo.
echo Waiting for server (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo [3/3] Opening Frontend in Browser...
start "" "G:\Hamdo\frontend\index.html"
echo [OK] Frontend opened

echo.
echo ========================================
echo    All services started successfully!
echo ========================================
echo.
echo  Backend API:  http://localhost:8000
echo  API Docs:     http://localhost:8000/docs
echo  Frontend:     Opened in browser
echo.
echo  Default Login:
echo    Username: admin
echo    Password: admin123
echo.
echo ========================================
echo  Close this window when done
echo ========================================
pause
