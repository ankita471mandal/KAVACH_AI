@echo off
title Kavach AI - Startup
color 0A

echo ============================================================
echo           KAVACH AI - Disaster Management System
echo ============================================================
echo.

echo [1/3] Starting Backend Server...
start "Kavach Backend" cmd /k "cd backend && venv\Scripts\activate && python run_server.py"

echo [2/3] Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo [3/3] Starting Frontend Dashboard...
start "Kavach Frontend" cmd /k "cd frontend && npm start"

echo.
echo ============================================================
echo                    KAVACH AI STARTED
echo ============================================================
echo.
echo  Backend API:       http://localhost:8000/docs
echo  Frontend App:      http://localhost:3000
echo  Health Check:      http://localhost:8000/health
echo.
echo ============================================================
echo.
echo Press any key to open integration test...
pause >nul

start cmd /k "cd backend && venv\Scripts\activate && python test_integration_complete.py"

echo.
echo All services started successfully!
echo Close this window or press Ctrl+C to exit
pause