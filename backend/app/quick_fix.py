"""
Quick fix for all common issues
"""
import os

print("🔧 Quick Fix Script\n")

# 1. Create missing __init__.py files
print("📁 Creating __init__.py files...")
init_files = [
    "app/__init__.py",
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/endpoints/__init__.py",
    "app/core/__init__.py",
    "app/db/__init__.py",
    "app/models/__init__.py",
    "app/schemas/__init__.py",
]

for file_path in init_files:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("# Package initialization\n")
        print(f"  ✅ Created {file_path}")
    else:
        print(f"  ✓ {file_path} exists")

# 2. Fix metadata in household model
print("\n🔧 Fixing household model...")
household_model = "app/models/household.py"
if os.path.exists(household_model):
    with open(household_model, "r") as f:
        content = f.read()
    
    if "metadata = Column" in content:
        content = content.replace("metadata = Column", "extra_data = Column")
        with open(household_model, "w") as f:
            f.write(content)
        print("  ✅ Fixed metadata -> extra_data in household.py")
    else:
        print("  ✓ household.py already fixed")

# 3. Fix metadata in rescue_report model
print("\n🔧 Fixing rescue_report model...")
rescue_model = "app/models/rescue_report.py"
if os.path.exists(rescue_model):
    with open(rescue_model, "r") as f:
        content = f.read()
    
    if "metadata = Column" in content:
        content = content.replace("metadata = Column", "extra_data = Column")
        with open(rescue_model, "w") as f:
            f.write(content)
        print("  ✅ Fixed metadata -> extra_data in rescue_report.py")
    else:
        print("  ✓ rescue_report.py already fixed")

print("\n✅ Quick fix complete!")
print("\nNext steps:")
print("  1. python run_init_db.py")
print("  2. python run_server.py")
print("  3. Open http://localhost:8000/docs")