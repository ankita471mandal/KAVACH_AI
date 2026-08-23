Write-Host "🔧 Kavach AI - Clean Installation" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green

# Remove old venv
if (Test-Path "venv") {
    Write-Host "Removing old virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

# Create new venv
Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow

pip install fastapi==0.115.0
pip install "uvicorn[standard]==0.32.1"
pip install sqlalchemy==2.0.35
pip install pydantic==2.10.3
pip install pydantic-settings==2.6.1
pip install email-validator==2.2.0
pip install python-dotenv==1.0.1
pip install httpx==0.28.1
pip install requests==2.32.3
pip install aiosqlite==0.20.0

Write-Host ""
Write-Host "✅ Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. python run_init_db.py" -ForegroundColor White
Write-Host "  2. python run_server.py" -ForegroundColor White