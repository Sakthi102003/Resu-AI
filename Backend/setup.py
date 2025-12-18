#!/usr/bin/env python
"""
Setup script for ResuAI Backend
Helps configure the environment and check dependencies
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path


def print_banner():
    print("""
    ╔═══════════════════════════════════════╗
    ║   ResuAI Backend Setup Script         ║
    ║   AI-Powered Resume Builder           ║
    ╚═══════════════════════════════════════╝
    """)


def check_python_version():
    """Check if Python version is 3.9 or higher"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Error: Python 3.9+ required. You have {version.major}.{version.minor}")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_env_file():
    """Create .env file from example if it doesn't exist"""
    print("\n✓ Setting up environment file...")
    
    env_file = Path(".env")
    example_file = Path(".env.example")
    
    if env_file.exists():
        print("  ✓ .env file already exists")
        return True
    
    if not example_file.exists():
        print("  ❌ .env.example not found")
        return False
    
    # Copy example to .env
    with open(example_file, 'r') as f:
        content = f.read()
    
    # Generate a secure secret key
    secret_key = secrets.token_hex(32)
    content = content.replace('your-secret-key-change-this-in-production-use-openssl-rand-hex-32', secret_key)
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("  ✓ Created .env file with secure SECRET_KEY")
    print("\n  ⚠️  IMPORTANT: Please edit .env and add your API keys:")
    print("     - MONGODB_URL (if using remote MongoDB)")
    print("     - OPENAI_API_KEY or GEMINI_API_KEY")
    
    return True


def install_dependencies():
    """Install Python dependencies"""
    print("\n✓ Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("  ✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("  ❌ Failed to install dependencies")
        return False


def check_mongodb():
    """Check if MongoDB is accessible"""
    print("\n✓ Checking MongoDB connection...")
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        
        # Try to connect
        async def test_connection():
            client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
            try:
                await client.server_info()
                return True
            except Exception:
                return False
            finally:
                client.close()
        
        connected = asyncio.run(test_connection())
        
        if connected:
            print("  ✓ MongoDB is running and accessible")
        else:
            print("  ⚠️  MongoDB not accessible at localhost:27017")
            print("     You can use MongoDB Atlas by setting MONGODB_URL in .env")
        
        return True
    except ImportError:
        print("  ⚠️  Cannot check MongoDB (motor not installed yet)")
        return True


def print_next_steps():
    """Print next steps for the user"""
    print("""
    ╔═══════════════════════════════════════╗
    ║   Setup Complete! 🎉                  ║
    ╚═══════════════════════════════════════╝

    Next Steps:
    
    1. Edit .env file and add your API keys:
       - OPENAI_API_KEY=your-key-here (or GEMINI_API_KEY)
       - Update MONGODB_URL if using remote MongoDB
    
    2. Start the server:
       python main.py
       
       Or with uvicorn:
       uvicorn main:app --reload
    
    3. Visit the API documentation:
       http://localhost:8000/docs
    
    4. Set up the frontend (in separate terminal):
       cd ../Frontend
       npm install
       npm run dev
    
    Happy coding! 🚀
    """)


def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n❌ Setup failed: Could not create .env file")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Check MongoDB (optional)
    check_mongodb()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
