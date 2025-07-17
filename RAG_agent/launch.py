#!/usr/bin/env python3
"""
Python launcher for the RAG Streamlit application
"""
import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit', 'plotly', 'pandas', 'chromadb', 
        'openai', 'pymupdf', 'beautifulsoup4'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 RAG Document Query System Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ Error: streamlit_app.py not found!")
        print("   Please run this script from the agent directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check OpenAI API key
    try:
        from config import openai_key
        if not openai_key:
            print("⚠️  Warning: OpenAI API key not found in config.py")
            print("   Please set your API key in config.py")
    except ImportError:
        print("❌ Error: config.py not found!")
        sys.exit(1)
    
    print("✅ All requirements met!")
    print("🌐 Starting Streamlit app...")
    print("   The app will open at: http://localhost:8501")
    print("   Press Ctrl+C to stop the server")
    print()
    
    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

if __name__ == "__main__":
    main()
