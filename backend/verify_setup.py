print("🔍 Verifying Kavach AI Backend Setup...\n")

# Check Python version
import sys
print(f"✅ Python Version: {sys.version}")

# Check Pydantic
try:
    import pydantic
    print(f"✅ Pydantic: {pydantic.__version__}")
except ImportError:
    print("❌ Pydantic not installed")

# Check email-validator
try:
    import email_validator
    print(f"✅ email-validator: {email_validator.__version__}")
except ImportError:
    print("❌ email-validator not installed - Run: pip install email-validator")

# Check FastAPI
try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError:
    print("❌ FastAPI not installed")

# Check SQLAlchemy
try:
    import sqlalchemy
    print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
except ImportError:
    print("❌ SQLAlchemy not installed")

print("\n🧪 Testing schema imports...")

try:
    from app.schemas import HazardCreate, HouseholdCreate, SOSCreate
    print("✅ All schemas imported successfully")
except Exception as e:
    print(f"❌ Schema import failed: {e}")

print("\n✅ Setup verification complete!")