#!/usr/bin/env python3
"""
Test script to verify multiple Streamlit instances can run simultaneously
"""
import subprocess
import sys
import time
import socket
import os
from pathlib import Path

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return False
        except socket.error:
            return True

def test_multiple_streamlit_instances():
    """Test launching multiple Streamlit instances"""
    print("=== Testing Multiple Streamlit Instances ===\n")
    
    # Test apps and ports
    test_apps = [
        ("smart_document_assistant.py", 8501),
        ("ai_math_tutor.py", 8502)
    ]
    
    processes = []
    
    for app_file, port in test_apps:
        if not Path(app_file).exists():
            print(f"❌ {app_file} not found, skipping...")
            continue
            
        if is_port_in_use(port):
            print(f"⚠️ Port {port} already in use, skipping {app_file}")
            continue
        
        print(f"🚀 Starting {app_file} on port {port}...")
        
        # Launch with improved command
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", str(port),
            "--server.headless", "true",
            "--server.runOnSave", "false",
            "--browser.serverAddress", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        
        try:
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            processes.append((process, app_file, port))
            print(f"✅ {app_file} process started (PID: {process.pid})")
        except Exception as e:
            print(f"❌ Failed to start {app_file}: {e}")
    
    if not processes:
        print("❌ No processes started successfully")
        return
    
    # Wait for apps to start
    print("\n⏳ Waiting for apps to start...")
    time.sleep(10)
    
    # Check if apps are running
    print("\n=== Checking App Status ===")
    for process, app_file, port in processes:
        if process.poll() is None:  # Process is still running
            if is_port_in_use(port):
                print(f"✅ {app_file} is running on port {port}")
                print(f"   Access at: http://localhost:{port}")
            else:
                print(f"⚠️ {app_file} process running but port {port} not responsive")
        else:
            print(f"❌ {app_file} process terminated")
    
    # Ask user if they want to keep apps running
    print("\n" + "="*50)
    print("Apps are now running. Check your browser at:")
    for process, app_file, port in processes:
        if process.poll() is None and is_port_in_use(port):
            print(f"  - http://localhost:{port} ({app_file})")
    
    input("\nPress Enter to stop all apps...")
    
    # Clean up processes
    print("\n🛑 Stopping all processes...")
    for process, app_file, port in processes:
        if process.poll() is None:
            process.terminate()
            print(f"✅ Stopped {app_file}")
        
    print("✅ All processes stopped")

if __name__ == "__main__":
    test_multiple_streamlit_instances()
