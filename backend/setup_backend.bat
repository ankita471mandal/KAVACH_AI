@echo off
echo ============================================================
echo Kavach AI - Backend Setup
echo ============================================================

echo.
echo [1/5] Removing old virtual environment...
if exist venv rmdir /s /q venv

echo [2/5] Creating new virtual environment...
python -m venv venv

echo [3/5] Activating virtual environment...
call venv\Scripts\activate

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip

echo [5/5] Installing dependencies...
pip install fastapi==0.115.0
pip install uvicorn[standard]==0.32.1
pip install sqlalchemy==2.0.35
pip install pydantic==2.10.3
pip install pydantic-settings==2.6.1
pip install email-validator==2.2.0
pip install python-dotenv==1.0.1
pip install httpx==0.28.1
pip install requests==2.32.3
pip install aiosqlite==0.20.0

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. python run_init_db.py
echo   2. python run_server.py
echo.
pause