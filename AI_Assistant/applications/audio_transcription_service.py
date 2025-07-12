#!/usr/bin/env python3
"""
Audio Transcription & Analysis Service
Upload audio files to get transcriptions, summaries, and insights
"""

import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path to import the agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import react_graph
from langchain_core.messages import HumanMessage

def main():
    st.set_page_config(
        page_title="Audio Transcription Service",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 Audio Transcription & Analysis Service")
    st.markdown("### Upload audio files for transcription, summarization, and analysis")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("🎧 Upload Audio File")
        uploaded_audio = st.file_uploader(
            "Choose an audio file",
            type=['mp3', 'wav', 'm4a', 'flac'],
            help="Supported formats: MP3, WAV, M4A, FLAC"
        )
        
        if uploaded_audio:
            st.success(f"✅ Audio uploaded: {uploaded_audio.name}")
            st.info(f"📊 File size: {uploaded_audio.size / 1024 / 1024:.2f} MB")
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if uploaded_audio:
            st.header("🎯 What would you like to do?")
            
            # Service options
            service_type = st.selectbox(
                "Choose a service:",
                [
                    "📝 Basic Transcription",
                    "📋 Transcription + Summary",
                    "🔍 Extract Key Information",
                    "💬 Meeting Analysis",
                    "🎓 Lecture Notes",
                    "📞 Interview Analysis",
                    "🎶 Custom Analysis"
                ]
            )
            
            # Custom question for detailed analysis
            if service_type == "🎶 Custom Analysis":
                custom_question = st.text_area(
                    "What specific information do you want to extract?",
                    placeholder="Examples:\n- What are the main action items discussed?\n- Who are the speakers and what are their roles?\n- What decisions were made?\n- What are the key quotes or statements?"
                )
            
            # Process button
            if st.button("🎵 Process Audio", type="primary"):
                with st.spinner("🤖 Processing audio... This may take a few minutes for large files."):
                    try:
                        # Save uploaded file temporarily with proper file handling
                        temp_file_path = None
                        try:
                            # Create temporary file with the same extension as uploaded file
                            file_extension = Path(uploaded_audio.name).suffix
                            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                                tmp_file.write(uploaded_audio.getvalue())
                                temp_file_path = tmp_file.name
                            
                            # Verify file was created successfully
                            if not os.path.exists(temp_file_path):
                                st.error("❌ Failed to create temporary file")
                                return
                            
                            # Display file info
                            st.info(f"📁 Processing file: {uploaded_audio.name} ({uploaded_audio.size / 1024 / 1024:.2f} MB)")
                            
                            # Prepare question based on service type
                            if service_type == "📝 Basic Transcription":
                                question = "Transcribe this audio file accurately. Return only the transcribed text."
                            elif service_type == "📋 Transcription + Summary":
                                question = "Transcribe this audio file and then provide a clear summary of the main points discussed."
                            elif service_type == "🔍 Extract Key Information":
                                question = "Transcribe this audio and extract key information including: main topics, important dates/numbers, key decisions, and action items."
                            elif service_type == "💬 Meeting Analysis":
                                question = "Transcribe this meeting audio and provide: 1) Summary of discussion, 2) Key decisions made, 3) Action items and who's responsible, 4) Next steps."
                            elif service_type == "🎓 Lecture Notes":
                                question = "Transcribe this lecture audio and create structured notes including: main topics, key concepts, important examples, and takeaways."
                            elif service_type == "📞 Interview Analysis":
                                question = "Transcribe this interview and provide: 1) Main topics discussed, 2) Key quotes and insights, 3) Summary of responses to each question."
                            elif service_type == "🎶 Custom Analysis":
                                question = f"Transcribe this audio file and then answer this specific question: {custom_question}"
                            
                            # Process with agent
                            st.info("🎧 Starting transcription...")
                            result = react_graph.invoke({
                                "messages": [HumanMessage(content=question)],
                                "input_file": temp_file_path
                            })
                            
                            # Display results
                            if result and "messages" in result:
                                final_message = result["messages"][-1]
                                response = final_message.content if hasattr(final_message, 'content') else str(final_message)
                                
                                st.subheader("🎯 Results:")
                                st.write(response)
                                
                                # Option to download transcription
                                st.download_button(
                                    label="📥 Download Transcription",
                                    data=response,
                                    file_name=f"transcription_{uploaded_audio.name}.txt",
                                    mime="text/plain"
                                )
                                
                                # Show processing details in expander
                                with st.expander("🔍 Processing Details"):
                                    st.write("**Service Used:**", service_type)
                                    st.write("**File:**", uploaded_audio.name)
                                    st.write("**Size:**", f"{uploaded_audio.size / 1024 / 1024:.2f} MB")
                                    st.write("**Temp File Path:**", temp_file_path)
                            else:
                                st.error("❌ No response received from the AI agent")
                        
                        finally:
                            # Clean up temp file
                            if temp_file_path and os.path.exists(temp_file_path):
                                try:
                                    os.unlink(temp_file_path)
                                    st.success("✅ Temporary file cleaned up")
                                except Exception as cleanup_error:
                                    st.warning(f"⚠️ Could not delete temporary file: {cleanup_error}")
                        
                    except Exception as e:
                        st.error(f"❌ Error processing audio: {str(e)}")
                        st.error("Please make sure the audio file is valid and try again.")
                        
                        # Debug information
                        with st.expander("🔧 Debug Information"):
                            st.write("**Error Details:**", str(e))
                            st.write("**File Name:**", uploaded_audio.name)
                            st.write("**File Size:**", uploaded_audio.size)
                            st.write("**File Type:**", uploaded_audio.type)
                            if temp_file_path:
                                st.write("**Temp File Path:**", temp_file_path)
                                st.write("**Temp File Exists:**", os.path.exists(temp_file_path) if temp_file_path else "N/A")
        
        else:
            st.header("🎵 Audio Transcription Services")
            st.markdown("""
            **Welcome to our AI-powered audio transcription service!**
            
            Upload any audio file and choose from our available services:
            
            📝 **Basic Transcription** - Convert speech to text accurately
            
            📋 **Transcription + Summary** - Get both full text and a summary
            
            🔍 **Extract Key Information** - Pull out important details, dates, and decisions
            
            💬 **Meeting Analysis** - Perfect for business meetings with action items
            
            🎓 **Lecture Notes** - Structured notes from educational content
            
            📞 **Interview Analysis** - Extract insights and key quotes
            
            🎶 **Custom Analysis** - Ask specific questions about your audio content
            
            ---
            
            **Supported formats:** MP3, WAV, M4A, FLAC
            
            **Use cases:**
            - Business meetings and conferences
            - Educational lectures and seminars  
            - Interviews and podcasts
            - Voice memos and recordings
            - Phone calls and webinars
            """)
    
    with col2:
        st.header("🛠️ Service Features")
        st.markdown("""
        **🎯 Accurate Transcription**
        - High-quality speech-to-text
        - Multiple speaker detection
        - Handles various accents
        
        **📊 Smart Analysis**
        - Automatic summarization
        - Key point extraction
        - Action item identification
        
        **💼 Business Ready**
        - Meeting transcription
        - Conference calls
        - Interview processing
        
        **🎓 Educational Support**
        - Lecture notes
        - Study materials
        - Research interviews
        
        **📱 Easy to Use**
        - Drag & drop upload
        - Multiple output formats
        - Download results
        """)
        
        st.header("📊 Pricing")
        st.markdown("""
        **Free Tier:**
        - Up to 10 minutes per file
        - Basic transcription
        - Summary included
        
        **Pro Features:**
        - Longer audio files
        - Advanced analysis
        - Custom questions
        - Priority processing
        """)
        
        st.header("🔒 Privacy & Security")
        st.markdown("""
        - Files processed securely
        - No permanent storage
        - GDPR compliant
        - Encrypted transmission
        """)

if __name__ == "__main__":
    main()
