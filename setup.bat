@echo off
chcp 65001 >nul
title Hamdo - First Time Setup

echo ========================================
echo    Hamdo - First Time Setup
echo ========================================
echo.

echo This script will:
echo   1. Create MySQL database
echo   2. Install Python dependencies
echo   3. Seed database with sample data
echo.
pause

echo.
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found. Please install Python 3.12+
    pause
    exit /b 1
)
echo [✓] Python found

echo.
echo [2/4] Creating virtual environment...
if not exist "G:\Hamdo\venv" (
    python -m venv venv
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment exists
)

echo.
echo [3/4] Installing dependencies...
call venv\Scripts\pip install -r requirements.txt
echo [✓] Dependencies installed

echo.
echo [4/4] Creating database and seeding data...
echo Make sure MySQL is running in XAMPP!
pause

call venv\Scripts\python.exe -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='', charset='utf8mb4'); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS jewelry_db'); conn.close(); print('[✓] Database created')"

call venv\Scripts\python.exe seeder.py

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo You can now run 'start.bat' to launch the application.
echo.
pause
