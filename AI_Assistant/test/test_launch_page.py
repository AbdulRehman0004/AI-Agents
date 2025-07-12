#!/usr/bin/env python3
"""
Test script to verify the launch page works correctly
"""
import socket
import sys
from pathlib import Path

def test_port_checker():
    """Test the port checking functionality"""
    print("Testing port checking...")
    
    # Test with a port that should be free
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return False
            except socket.error:
                return True
    
    # Test with a random high port
    test_port = 9999
    result = is_port_in_use(test_port)
    print(f"Port {test_port} in use: {result}")
    
    # Test with a commonly used port
    test_port = 80
    result = is_port_in_use(test_port)
    print(f"Port {test_port} in use: {result}")

def test_file_existence():
    """Test if all required files exist"""
    print("\nTesting file existence...")
    
    required_files = [
        "smart_document_assistant.py",
        "ai_math_tutor.py", 
        "audio_transcription_service.py",
        "data_analysis_assistant.py",
        "unified_ai_assistant_new.py"
    ]
    
    for file in required_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file}: {'Found' if exists else 'Not Found'}")

def test_streamlit_import():
    """Test if streamlit can be imported"""
    print("\nTesting Streamlit import...")
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
        print(f"   Version: {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")

def main():
    print("=== AI Assistant Suite Test ===")
    test_port_checker()
    test_file_existence()
    test_streamlit_import()
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
