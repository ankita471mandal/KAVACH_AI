"""
Complete fix script - Run this to fix everything
"""
import os
import sys

print("="*60)
print("🔧 KAVACH AI - Complete Fix Script")
print("="*60)

# Step 1: Create directories
print("\n📁 Step 1: Creating directories...")
directories = [
    "app/api/v1/endpoints",
    "app/core",
    "app/db",
    "app/models",
    "app/schemas",
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    init_file = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, "w").close()

print("✅ Directories created")

# Step 2: Check user model exists
print("\n📄 Step 2: Checking user model...")
user_model_path = "app/models/user.py"
if not os.path.exists(user_model_path):
    print(f"⚠️  Creating {user_model_path}")
    with open(user_model_path, "w") as f:
        f.write('''from sqlalchemy import Column, Integer, String, Boolean
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), default="citizen")
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String(255), nullable=False)
''')
else:
    print("✅ User model exists")

# Step 3: Test imports
print("\n🧪 Step 3: Testing imports...")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.models import User
    print("✅ Imports working")
except Exception as e:
    print(f"❌ Import error: {e}")
    print("\nPlease check:")
    print("1. All model files exist in app/models/")
    print("2. app/models/__init__.py imports all models")
    sys.exit(1)

# Step 4: Instructions
print("\n" + "="*60)
print("✅ Fix complete!")
print("="*60)
print("\nNext steps:")
print("1. Run: python run_init_db.py")
print("2. Run: python run_server.py")
print("3. Open: http://localhost:8000/docs")
print("="*60)