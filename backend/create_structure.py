"""
Create complete file structure for backend
"""
import os

# Create all directories
directories = [
    "app",
    "app/api",
    "app/api/v1",
    "app/api/v1/endpoints",
    "app/core",
    "app/db",
    "app/models",
    "app/schemas",
]

print("📁 Creating directory structure...\n")

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    
    # Create __init__.py in each directory
    init_file = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("# Package initialization\n")
        print(f"✅ Created {init_file}")

print("\n✅ Directory structure created!")