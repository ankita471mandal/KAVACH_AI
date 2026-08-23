"""
File structure verification
"""
import os

required_files = {
    "Models": [
        "app/models/__init__.py",
        "app/models/base.py",
        "app/models/user.py",
        "app/models/household.py",
        "app/models/hazard.py",
        "app/models/hospital.py",
        "app/models/shelter.py",
        "app/models/road.py",
        "app/models/rescue_report.py",
        "app/models/sos_request.py",
        "app/models/zone.py",
    ],
    "Schemas": [
        "app/schemas/__init__.py",
        "app/schemas/household.py",
        "app/schemas/hazard.py",
        "app/schemas/hospital.py",
        "app/schemas/shelter.py",
        "app/schemas/road.py",
        "app/schemas/rescue.py",
        "app/schemas/sos.py",
        "app/schemas/zone.py",
        "app/schemas/user.py",
    ],
    "Endpoints": [
        "app/api/__init__.py",
        "app/api/v1/__init__.py",
        "app/api/v1/endpoints/__init__.py",
        "app/api/v1/endpoints/hazards.py",
        "app/api/v1/endpoints/households.py",
        "app/api/v1/endpoints/hospitals.py",
        "app/api/v1/endpoints/shelters.py",
        "app/api/v1/endpoints/roads.py",
        "app/api/v1/endpoints/rescue.py",
        "app/api/v1/endpoints/sos.py",
        "app/api/v1/endpoints/zones.py",
    ],
    "Core": [
        "app/core/__init__.py",
        "app/core/config.py",
        "app/db/__init__.py",
        "app/db/session.py",
        "app/main.py",
    ]
}

print("🔍 Checking File Structure...\n")

missing_files = []
for category, files in required_files.items():
    print(f"📁 {category}:")
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
    print()

if missing_files:
    print(f"\n⚠️  {len(missing_files)} files are missing!")
    print("\nMissing files:")
    for f in missing_files:
        print(f"  • {f}")
else:
    print("✅ All files present!")