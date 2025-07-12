#!/usr/bin/env python3
"""
AI Assistant Suite - Landing Page
A beautiful landing page to launch individual AI applications
"""

import streamlit as st
import subprocess
import sys
import os
import time
import socket
from pathlib import Path

def main():
    st.set_page_config(
        page_title="AI Assistant Suite",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for beautiful design
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .app-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .app-card h3 {
        color: #333;
        margin-bottom: 1rem;
    }
    
    .app-card p {
        color: #666;
        margin-bottom: 1rem;
    }
    
    .feature-list {
        color: #555;
        font-size: 0.9rem;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.markdown('<h1 class="main-title">🤖 AI Assistant Suite</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 3rem;">Choose your AI-powered application</p>', unsafe_allow_html=True)
    
    # Create two columns for the app cards
    col1, col2 = st.columns(2)
    
    with col1:
        # Document Assistant Card
        st.markdown("""
        <div class="app-card">
            <h3>📚 Smart Document Assistant</h3>
            <p>Upload and analyze documents with AI-powered insights</p>
            <div class="feature-list">
                • PDF, Word, Excel, PowerPoint support<br>
                • OCR for images and scanned documents<br>
                • Question-answering about content<br>
                • Document summarization
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Document Assistant", key="doc", use_container_width=True, type="primary"):
            launch_app("smart_document_assistant.py", "Document Assistant", 8501)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Math Tutor Card
        st.markdown("""
        <div class="app-card">
            <h3>🧮 AI Math Tutor</h3>
            <p>Solve mathematical problems with step-by-step explanations</p>
            <div class="feature-list">
                • Symbolic mathematics with SymPy<br>
                • Unit conversions<br>
                • Step-by-step solutions<br>
                • Educational explanations
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Math Tutor", key="math", use_container_width=True, type="primary"):
            launch_app("ai_math_tutor.py", "Math Tutor", 8502)
    
    with col2:
        # Audio Transcription Card
        st.markdown("""
        <div class="app-card">
            <h3>🎵 Audio Transcription</h3>
            <p>High-quality audio transcription with content analysis</p>
            <div class="feature-list">
                • OpenAI Whisper transcription<br>
                • Multiple audio formats<br>
                • Content analysis and summarization<br>
                • Key topic extraction
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Audio Transcription", key="audio", use_container_width=True, type="primary"):
            launch_app("audio_transcription_service.py", "Audio Transcription", 8503)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Data Analysis Card
        st.markdown("""
        <div class="app-card">
            <h3>📊 Data Analysis Assistant</h3>
            <p>Intelligent data processing with statistical insights</p>
            <div class="feature-list">
                • CSV, Excel, JSON processing<br>
                • Statistical analysis<br>
                • Trend identification<br>
                • Automated reporting
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Data Analysis", key="data", use_container_width=True, type="primary"):
            launch_app("data_analysis_assistant.py", "Data Analysis", 8504)
    
    # Quick actions section
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🚀 Launch All Apps", use_container_width=True):
            launch_all_apps()
    
    with action_col2:
        if st.button("📖 View Documentation", use_container_width=True):
            show_documentation()
    
    with action_col3:
        if st.button("⚙️ System Status", use_container_width=True):
            show_system_status()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🤖 AI Assistant Suite v2.0 | Built with Streamlit & OpenAI</p>
        <p>Click any launch button to start the corresponding application</p>
    </div>
    """, unsafe_allow_html=True)

def launch_app(app_file, app_name, port):
    """Launch a Streamlit app on a specific port"""
    try:
        # Check if the app file exists
        if not Path(app_file).exists():
            st.error(f"❌ App file not found: {app_file}")
            return
        
        # Check if port is already in use
        if is_port_in_use(port):
            st.warning(f"⚠️ Port {port} is already in use. The app might already be running.")
            st.info(f"📱 Try accessing: http://localhost:{port}")
            st.markdown(f"""
            <a href="http://localhost:{port}" target="_blank" style="
                display: inline-block;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 10px;
            ">🌐 Open {app_name}</a>
            """, unsafe_allow_html=True)
            return
        
        # Launch the app with additional flags for multiple instances
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_file, 
            "--server.port", str(port),
            "--server.headless", "true",
            "--server.runOnSave", "false",
            "--browser.serverAddress", "localhost",
            "--browser.gatherUsageStats", "false"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        
        # Show launching message with progress
        st.success(f"🚀 {app_name} is starting...")
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Wait for the app to start with progress updates
        max_wait = 20  # 20 seconds max
        for i in range(max_wait):
            progress = (i + 1) / max_wait
            progress_bar.progress(progress)
            
            if is_port_in_use(port):
                progress_bar.progress(1.0)
                status_text.success(f"✅ {app_name} is ready!")
                break
            else:
                status_text.info(f"⏳ Starting {app_name}... ({i+1}/{max_wait} seconds)")
                time.sleep(1)
        else:
            # If we exit the loop without breaking, app failed to start
            status_text.error(f"❌ {app_name} failed to start within {max_wait} seconds. Please try again.")
            return
        
        # Add clickable link (app is now ready)
        st.markdown(f"""
        <a href="http://localhost:{port}" target="_blank" style="
            display: inline-block;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 10px;
            font-size: 16px;
            font-weight: bold;
        ">🌐 Open {app_name}</a>
        """, unsafe_allow_html=True)
        
        st.balloons()  # Celebrate successful launch
        st.success("🎉 Your app is now ready! Click the link above to access it.")
        
    except Exception as e:
        st.error(f"❌ Error launching {app_name}: {str(e)}")

def is_port_in_use(port):
    """Check if a port is already in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return False
        except socket.error:
            return True

def launch_all_apps():
    """Launch all applications at once"""
    apps = [
        ("smart_document_assistant.py", "Document Assistant", 8501),
        ("ai_math_tutor.py", "Math Tutor", 8502),
        ("audio_transcription_service.py", "Audio Transcription", 8503),
        ("data_analysis_assistant.py", "Data Analysis", 8504)
    ]
    
    st.info("🚀 Launching all applications...")
    
    # Create a progress bar for all apps
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    launched_apps = []
    for i, (app_file, app_name, port) in enumerate(apps):
        progress = (i + 1) / len(apps)
        status_text.info(f"Processing {app_name}...")
        
        if Path(app_file).exists():
            if not is_port_in_use(port):
                try:
                    cmd = [
                        sys.executable, "-m", "streamlit", "run", app_file, 
                        "--server.port", str(port),
                        "--server.headless", "true",
                        "--server.runOnSave", "false",
                        "--browser.serverAddress", "localhost",
                        "--browser.gatherUsageStats", "false"
                    ]
                    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
                    st.success(f"✅ {app_name}: Starting on port {port}")
                    launched_apps.append((app_name, port))
                except Exception as e:
                    st.error(f"❌ {app_name}: {str(e)}")
            else:
                st.info(f"ℹ️ {app_name}: Already running on port {port}")
                launched_apps.append((app_name, port))
        else:
            st.warning(f"⚠️ {app_name}: File not found")
        
        progress_bar.progress(progress)
    
    status_text.success("✅ All applications processed!")
    
    if launched_apps:
        st.info("⏳ Please wait 10-15 seconds for all apps to fully load before accessing them.")
        
        # Show all the links
        st.markdown("### 🌐 Access Links:")
        for app_name, port in launched_apps:
            st.markdown(f"""
            <a href="http://localhost:{port}" target="_blank" style="
                display: inline-block;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                text-decoration: none;
                margin: 5px;
                font-size: 14px;
            ">🌐 {app_name}</a>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ No applications were launched successfully.")

def show_documentation():
    """Show documentation"""
    with st.expander("📖 Documentation", expanded=True):
        st.markdown("""
        ### Getting Started
        1. Click any "🚀 Launch" button to start an application
        2. Each app opens in a new browser tab on different ports
        3. Apps run independently and can be used simultaneously
        
        ### Applications
        - **Document Assistant** (Port 8501): Analyze documents, PDFs, images
        - **Math Tutor** (Port 8502): Solve math problems with explanations
        - **Audio Transcription** (Port 8503): Convert audio to text
        - **Data Analysis** (Port 8504): Analyze CSV/Excel data
        
        ### Tips
        - Each app remembers your session data
        - You can run multiple apps at the same time
        - If a port is busy, try restarting the app
        """)

def show_system_status():
    """Show system status"""
    with st.expander("⚙️ System Status", expanded=True):
        st.markdown("### Available Applications")
        
        apps = [
            "smart_document_assistant.py",
            "ai_math_tutor.py",
            "audio_transcription_service.py",
            "data_analysis_assistant.py"
        ]
        
        for app in apps:
            if Path(app).exists():
                st.markdown(f"✅ {app}")
            else:
                st.markdown(f"❌ {app} (not found)")
        
        st.markdown("### Port Configuration")
        st.markdown("- Landing Page: 8500")
        st.markdown("- Document Assistant: 8501")
        st.markdown("- Math Tutor: 8502")
        st.markdown("- Audio Transcription: 8503")
        st.markdown("- Data Analysis: 8504")

if __name__ == "__main__":
    main()
