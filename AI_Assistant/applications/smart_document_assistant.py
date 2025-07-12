#!/usr/bin/env python3
"""
Smart Document Assistant Web App
A simple Streamlit app that showcases your agent's document processing capabilities
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import sys

# Add the parent directory to the Python path to import the agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your agent
from agent import react_graph
from langchain_core.messages import HumanMessage

def main():
    st.set_page_config(
        page_title="Smart Document Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Smart Document Assistant")
    st.markdown("### Upload any document and ask questions about it!")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'pptx', 'xlsx', 'txt', 'csv', 'json', 'mp3', 'wav', 'png', 'jpg', 'jpeg'],
            help="Supported formats: PDF, Word, PowerPoint, Excel, Text, CSV, JSON, Audio, Images"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size} bytes")
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💭 Ask Questions")
        
        # Example questions based on file type
        if uploaded_file:
            file_ext = Path(uploaded_file.name).suffix.lower()
            
            if file_ext in ['.pdf', '.docx', '.txt']:
                examples = [
                    "Summarize the main points of this document",
                    "What are the key findings or conclusions?",
                    "Extract all the important dates and numbers",
                    "Who are the main people mentioned?"
                ]
            elif file_ext in ['.xlsx', '.csv']:
                examples = [
                    "What data is in this spreadsheet?",
                    "Calculate the total sum of the numerical columns",
                    "What trends can you identify in the data?",
                    "Create a summary of the statistics"
                ]
            elif file_ext in ['.pptx']:
                examples = [
                    "What is this presentation about?",
                    "List the main topics covered in each slide",
                    "What are the key takeaways?",
                    "Summarize the conclusion"
                ]
            elif file_ext in ['.mp3', '.wav']:
                examples = [
                    "Transcribe this audio file",
                    "What are the main topics discussed?",
                    "Extract any important quotes or statements",
                    "Summarize the conversation"
                ]
            elif file_ext in ['.png', '.jpg', '.jpeg']:
                examples = [
                    "What text is visible in this image?",
                    "Describe what you see in the image",
                    "Extract any data or numbers from the image",
                    "Is there any readable text or documents?"
                ]
            else:
                examples = ["What is the content of this file?"]
            
            st.subheader("💡 Example Questions:")
            for example in examples:
                if st.button(example, key=f"example_{hash(example)}"):
                    st.session_state.question = example
        
        # Question input
        question = st.text_area(
            "Your Question:",
            value=st.session_state.get('question', ''),
            height=100,
            placeholder="Ask anything about your uploaded document..."
        )
        
        # Process button
        if st.button("🔍 Analyze Document", type="primary") and question and uploaded_file:
            with st.spinner("🤖 Processing your question..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_file_path = tmp_file.name
                    
                    # Process with your agent
                    result = react_graph.invoke({
                        "messages": [HumanMessage(content=question)],
                        "input_file": temp_file_path
                    })
                    
                    # Display result
                    st.subheader("🤖 Agent Response:")
                    
                    # Get the final response
                    if result and "messages" in result:
                        final_message = result["messages"][-1]
                        response_content = final_message.content if hasattr(final_message, 'content') else str(final_message)
                        
                        st.write(response_content)
                        
                        # Show conversation history in expander
                        with st.expander("📝 Full Conversation History"):
                            for i, msg in enumerate(result["messages"]):
                                msg_content = msg.content if hasattr(msg, 'content') else str(msg)
                                st.text(f"Message {i+1}: {msg_content[:200]}...")
                    
                    # Clean up temp file
                    os.unlink(temp_file_path)
                    
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                    st.error("Please make sure the agent is properly configured.")
    
    with col2:
        st.header("🛠️ Agent Capabilities")
        st.markdown("""
        **Document Types:**
        - 📄 PDF files
        - 📝 Word documents
        - 📊 Excel spreadsheets  
        - 🎯 PowerPoint presentations
        - 🖼️ Images (OCR)
        - 🎵 Audio files (transcription)
        - 📋 Text, CSV, JSON files
        
        **What I can do:**
        - Extract and analyze content
        - Answer questions about documents
        - Summarize key information
        - Perform calculations on data
        - Transcribe audio content
        - Extract text from images
        - Search for specific information
        """)
        
        st.header("🎯 Use Cases")
        st.markdown("""
        - **Business**: Analyze reports, contracts, invoices
        - **Research**: Summarize papers, extract data
        - **Education**: Study materials, transcribe lectures
        - **Legal**: Review documents, extract clauses
        - **Finance**: Analyze spreadsheets, reports
        - **Media**: Transcribe interviews, analyze content
        """)

if __name__ == "__main__":
    # Initialize session state
    if 'question' not in st.session_state:
        st.session_state.question = ''
    
    main()
