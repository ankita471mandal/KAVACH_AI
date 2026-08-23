"""
Debug import issues
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Testing imports...\n")

try:
    print("1. Testing app.models.base...")
    from app.models.base import Base, BaseModel
    print("   ✅ Success\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

try:
    print("2. Testing app.models.user...")
    from app.models.user import User
    print("   ✅ Success\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

try:
    print("3. Testing app.models...")
    from app.models import User, Household, Hazard
    print("   ✅ Success\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

try:
    print("4. Testing app.db.session...")
    from app.db.session import engine, SessionLocal
    print("   ✅ Success\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

try:
    print("5. Testing app.main...")
    from app.main import app
    print("   ✅ Success\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

print("✅ Import test complete!")