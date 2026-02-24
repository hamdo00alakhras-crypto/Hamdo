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
    echo [!] MySQL service not found. Please start XAMPP MySQL manually.
    echo     Or run: net start MySQL
) else (
    echo [✓] MySQL service found
)

echo.
echo [2/3] Starting Backend Server (FastAPI)...
start "Hamdo Backend" cmd /k "cd /d G:\Hamdo && venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"
echo [✓] Backend starting on http://localhost:8000

echo.
timeout /t 3 /nobreak >nul

echo [3/3] Opening Frontend in Browser...
start "" "G:\Hamdo\frontend\index.html"
echo [✓] Frontend opened

echo.
echo ========================================
echo    All services started successfully!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend:     Opened in browser
echo.
echo Default Login:
echo   Username: admin
echo   Password: admin123
echo.
echo Press any key to open API Documentation...
pause >nul

start "" "http://localhost:8000/docs"

echo.
echo Press any key to exit this window...
echo (Backend server will keep running)
pause >nul
