"""
Streamlit web interface for the RAG system
"""
import streamlit as st
import os
import time
from pathlib import Path
import plotly.express as px
import pandas as pd

# Import our modules
from database import initialize_database, store_document_to_db
from query_engine import query_database, get_similar_documents
from document_processor import extract_text_from_file
from utils import validate_file_path, format_file_size, get_file_size, list_supported_files

# Page configuration
st.set_page_config(
    page_title="RAG Document Query System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
        background-color: #f0f2f6;
    }
    .user-message {
        background-color: #e8f4f8;
        border-left-color: #1f77b4;
    }
    .assistant-message {
        background-color: #f0f8e8;
        border-left-color: #2ca02c;
    }
    .document-info {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'database_initialized' not in st.session_state:
    st.session_state.database_initialized = False
if 'index' not in st.session_state:
    st.session_state.index = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

def initialize_system():
    """Initialize the RAG system"""
    try:
        with st.spinner("Initializing database..."):
            st.session_state.index = initialize_database()
            st.session_state.database_initialized = True
        st.success("✅ Database initialized successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Error initializing database: {str(e)}")
        return False

def upload_document(uploaded_file, doc_id=None):
    """Handle document upload"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Generate doc_id if not provided
        if not doc_id:
            doc_id = f"doc_{len(st.session_state.uploaded_documents) + 1}"
        
        # Store in database
        with st.spinner(f"Processing {uploaded_file.name}..."):
            success = store_document_to_db(temp_path, doc_id, st.session_state.index)
        
        if success:
            # Add to session state
            st.session_state.uploaded_documents.append({
                'name': uploaded_file.name,
                'doc_id': doc_id,
                'size': format_file_size(uploaded_file.size),
                'type': uploaded_file.type
            })
            st.success(f"✅ Document '{uploaded_file.name}' uploaded successfully!")
        else:
            st.error(f"❌ Failed to upload '{uploaded_file.name}'")
        
        # Clean up temporary file
        os.remove(temp_path)
        
    except Exception as e:
        st.error(f"❌ Error uploading document: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def add_to_chat(message, is_user=True):
    """Add message to chat history"""
    st.session_state.chat_history.append({
        'message': message,
        'is_user': is_user,
        'timestamp': time.time()
    })

def display_chat_history():
    """Display chat history"""
    for chat in st.session_state.chat_history:
        message_class = "user-message" if chat['is_user'] else "assistant-message"
        role = "🙋‍♂️ You" if chat['is_user'] else "🤖 Assistant"
        
        st.markdown(f"""
        <div class="chat-message {message_class}">
            <strong>{role}:</strong><br>
            {chat['message']}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">🔍 RAG Document Query System</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Initialize system button
        if not st.session_state.database_initialized:
            if st.button("🚀 Initialize System", type="primary"):
                initialize_system()
        else:
            st.success("✅ System Ready")
        
        # File upload
        if st.session_state.database_initialized:
            st.subheader("📤 Upload Documents")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['pdf', 'html'],
                help="Upload PDF or HTML files to add to the knowledge base"
            )
            
            if uploaded_file is not None:
                doc_id = st.text_input("Document ID (optional)", 
                                     value=f"doc_{len(st.session_state.uploaded_documents) + 1}")
                if st.button("Upload Document"):
                    upload_document(uploaded_file, doc_id)
            
            # Display uploaded documents
            if st.session_state.uploaded_documents:
                st.subheader("📚 Uploaded Documents")
                for doc in st.session_state.uploaded_documents:
                    with st.expander(f"📄 {doc['name']}"):
                        st.write(f"**ID:** {doc['doc_id']}")
                        st.write(f"**Size:** {doc['size']}")
                        st.write(f"**Type:** {doc['type']}")
        
        # Settings
        st.subheader("⚙️ Settings")
        similarity_k = st.slider("Similarity Top K", 1, 10, 3, 
                                help="Number of similar documents to retrieve")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    if not st.session_state.database_initialized:
        st.info("👈 Please initialize the system using the sidebar")
        return
    
    # Create two columns for chat and additional info
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("💬 Chat with Documents")
        
        # Chat input
        user_question = st.text_input("Ask a question about your documents:", 
                                    placeholder="What is the main purpose of the document?")
        
        if st.button("🚀 Ask", type="primary") and user_question:
            # Add user message to chat
            add_to_chat(user_question, is_user=True)
            
            # Get answer
            with st.spinner("Thinking..."):
                answer = query_database(user_question, st.session_state.index, k=similarity_k)
            
            # Add assistant response to chat
            add_to_chat(answer, is_user=False)
            
            # Rerun to show updated chat
            st.rerun()
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("📝 Chat History")
            display_chat_history()
    
    with col2:
        st.header("📊 Information")
        
        # Statistics
        if st.session_state.uploaded_documents:
            st.subheader("📈 Statistics")
            stats_data = {
                'Metric': ['Total Documents', 'Total Questions', 'Average Response Time'],
                'Value': [
                    len(st.session_state.uploaded_documents),
                    len([c for c in st.session_state.chat_history if c['is_user']]),
                    "< 1s"  # Placeholder
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, hide_index=True)
        
        # Document types chart
        if st.session_state.uploaded_documents:
            st.subheader("📁 Document Types")
            doc_types = {}
            for doc in st.session_state.uploaded_documents:
                ext = doc['name'].split('.')[-1].upper()
                doc_types[ext] = doc_types.get(ext, 0) + 1
            
            if doc_types:
                fig = px.pie(
                    values=list(doc_types.values()),
                    names=list(doc_types.keys()),
                    title="Document Types Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("📋 Show Similar Documents"):
            if st.session_state.chat_history:
                last_question = None
                for chat in reversed(st.session_state.chat_history):
                    if chat['is_user']:
                        last_question = chat['message']
                        break
                
                if last_question:
                    similar_docs = get_similar_documents(last_question, st.session_state.index, k=3)
                    if isinstance(similar_docs, list):
                        st.write("**Similar Documents:**")
                        for i, doc in enumerate(similar_docs, 1):
                            with st.expander(f"Document {i} (Score: {doc.get('score', 'N/A')})"):
                                st.write(doc.get('text', 'No text available')[:500] + "...")
                    else:
                        st.error(similar_docs)
        
        if st.button("💾 Export Chat History"):
            if st.session_state.chat_history:
                chat_text = ""
                for chat in st.session_state.chat_history:
                    role = "User" if chat['is_user'] else "Assistant"
                    chat_text += f"{role}: {chat['message']}\n\n"
                
                st.download_button(
                    label="Download Chat History",
                    data=chat_text,
                    file_name="chat_history.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
