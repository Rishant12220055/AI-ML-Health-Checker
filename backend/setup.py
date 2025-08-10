#!/usr/bin/env python3
"""
Setup script for AI Healthcare Assistant
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    print("=" * 60)
    print("  🏥 AI Healthcare Assistant Setup")
    print("=" * 60)
    print()

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/guidelines",
        "logs",
        "models",
        "models/transformers"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_env_file():
    """Create .env file from example"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        env_file.write_text(env_example.read_text())
        print("✓ Created .env file from example")
        print("  📝 Please edit .env file with your configuration")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("❌ .env.example not found")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        # Use the configured Python environment
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        print("✓ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True

def download_models():
    """Download required AI models"""
    print("\n🤖 Downloading AI models...")
    
    # This would download the models in a real setup
    # For now, we'll create placeholder files
    models_dir = Path("models")
    
    model_info = {
        "clinical_bert": {
            "name": "emilyalsentzer/Bio_ClinicalBERT",
            "status": "placeholder"
        },
        "sentence_transformer": {
            "name": "all-MiniLM-L6-v2", 
            "status": "placeholder"
        }
    }
    
    with open(models_dir / "model_info.json", "w") as f:
        json.dump(model_info, f, indent=2)
    
    print("✓ Model information saved")
    print("  📝 Models will be downloaded on first use")

def create_database_config():
    """Create database configuration"""
    print("\n💾 Setting up database configuration...")
    
    # Create sample data
    data_dir = Path("data")
    
    # Sample medical data
    sample_conditions = {
        "common_conditions": [
            {"name": "Common Cold", "symptoms": ["runny nose", "congestion", "sore throat"]},
            {"name": "Influenza", "symptoms": ["fever", "fatigue", "body aches", "cough"]},
            {"name": "Headache", "symptoms": ["head pain", "light sensitivity", "nausea"]}
        ]
    }
    
    with open(data_dir / "sample_conditions.json", "w") as f:
        json.dump(sample_conditions, f, indent=2)
    
    print("✓ Sample medical data created")

def main():
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Create environment file
    print("\n⚙️ Setting up configuration...")
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Download models
    download_models()
    
    # Setup database
    create_database_config()
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your configuration")
    print("2. Install and start MongoDB (if using local database)")
    print("3. Run the application:")
    print("   python main.py")
    print("\n4. Access the API documentation at:")
    print("   http://localhost:8000/docs")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
