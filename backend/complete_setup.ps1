# Complete Setup Script for Kavach AI Backend

Write-Host "=" -ForegroundColor Green
Write-Host "🚀 Kavach AI Backend - Complete Setup" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green

# Step 1: Check Python
Write-Host "`n📌 Step 1: Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Step 2: Create virtual environment
Write-Host "`n📌 Step 2: Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "ℹ️  Virtual environment already exists" -ForegroundColor Cyan
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate virtual environment
Write-Host "`n📌 Step 3: Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Step 4: Install dependencies
Write-Host "`n📌 Step 4: Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pydantic-settings email-validator
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Step 5: Initialize database
Write-Host "`n📌 Step 5: Initializing database..." -ForegroundColor Yellow
python run_init_db.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database initialized" -ForegroundColor Green
} else {
    Write-Host "❌ Database initialization failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n" + "="*60 -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green

Write-Host "`n📌 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Keep this terminal open" -ForegroundColor White
Write-Host "  2. Run: python run_server.py" -ForegroundColor Yellow
Write-Host "  3. Open browser: http://localhost:8000/docs" -ForegroundColor Yellow

Write-Host "`nPress any key to start server..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

python run_server.py