@echo off
chcp 65001 >nul
title Hamdo - Stop Services

echo ========================================
echo    Hamdo - Stopping Services
echo ========================================
echo.

echo [1/2] Stopping Python/Uvicorn processes...
taskkill /f /im python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Python processes stopped
) else (
    echo [!] No Python processes found
)

echo.
echo [2/2] Cleanup complete
echo.

echo ========================================
echo    All services stopped
echo ========================================
echo.
pause
