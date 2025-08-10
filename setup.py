#!/usr/bin/env python3
"""
Setup script for AI Healthcare Assistant

This script helps set up the development environment and install dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is supported")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} is installed")
            return True
    except:
        pass
    
    print("❌ Node.js is not installed")
    print("Please install Node.js 16+ from https://nodejs.org/")
    return False

def create_virtual_environment():
    """Create Python virtual environment"""
    venv_path = Path("backend/venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command(
        f"cd backend && python -m venv venv",
        "Creating Python virtual environment"
    )

def activate_venv_command():
    """Get the command to activate virtual environment based on OS"""
    if platform.system() == "Windows":
        return "backend\\venv\\Scripts\\activate"
    else:
        return "source backend/venv/bin/activate"

def install_python_dependencies():
    """Install Python dependencies"""
    if platform.system() == "Windows":
        pip_command = "backend\\venv\\Scripts\\pip"
    else:
        pip_command = "backend/venv/bin/pip"
    
    return run_command(
        f"{pip_command} install -r backend/requirements.txt",
        "Installing Python dependencies"
    )

def install_node_dependencies():
    """Install Node.js dependencies"""
    return run_command(
        "cd frontend && npm install",
        "Installing Node.js dependencies"
    )

def create_env_file():
    """Create .env file from example"""
    env_path = Path("backend/.env")
    env_example_path = Path("backend/.env.example")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example_path.exists():
        print("❌ .env.example file not found")
        return False
    
    try:
        with open(env_example_path, 'r') as src, open(env_path, 'w') as dst:
            dst.write(src.read())
        print("✅ Created .env file from example")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "backend/logs",
        "backend/data",
        "backend/data/guidelines",
        "backend/models",
        "backend/models/transformers"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created necessary directories")
    return True

def download_models():
    """Download and cache required AI models"""
    print("🔄 Downloading AI models (this may take a few minutes)...")
    
    # This would download the models in a real implementation
    # For now, we'll just create placeholder files
    models_dir = Path("backend/models")
    
    # Create model info file
    model_info = """
# AI Models for Healthcare Assistant

This directory will contain the downloaded AI models:

1. ClinicalBERT - For medical text understanding
2. Sentence Transformers - For semantic similarity
3. Custom medical knowledge embeddings

Models will be automatically downloaded on first use.
"""
    
    with open(models_dir / "README.md", "w") as f:
        f.write(model_info)
    
    print("✅ Model directory prepared")
    return True

def setup_database():
    """Setup instructions for MongoDB"""
    print("\n📋 Database Setup Instructions:")
    print("1. Install MongoDB Community Edition:")
    print("   - Windows: https://docs.mongodb.com/manual/installation/install-mongodb-on-windows/")
    print("   - macOS: brew install mongodb-community")
    print("   - Linux: https://docs.mongodb.com/manual/installation/install-mongodb-on-ubuntu/")
    print("2. Start MongoDB service:")
    print("   - Windows: Start the MongoDB service from Services")
    print("   - macOS/Linux: brew services start mongodb-community or systemctl start mongod")
    print("3. The application will connect to mongodb://localhost:27017 by default")
    print("4. You can change the connection string in the .env file")
    
def main():
    """Main setup function"""
    print("🏥 AI Healthcare Assistant Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Setup backend
    print("\n🐍 Setting up Python backend...")
    if not create_virtual_environment():
        sys.exit(1)
    
    if not install_python_dependencies():
        sys.exit(1)
    
    if not create_env_file():
        sys.exit(1)
    
    if not create_directories():
        sys.exit(1)
    
    if not download_models():
        sys.exit(1)
    
    # Setup frontend
    print("\n⚛️ Setting up React frontend...")
    if not install_node_dependencies():
        sys.exit(1)
    
    # Database setup instructions
    setup_database()
    
    # Success message
    print("\n✅ Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Start MongoDB service")
    print("2. Backend: Run 'python backend/main.py' to start the API server")
    print("3. Frontend: Run 'npm run dev' in the frontend directory")
    print("4. Open http://localhost:3000 in your browser")
    
    print(f"\n💡 To activate the Python environment:")
    print(f"   {activate_venv_command()}")

if __name__ == "__main__":
    main()
