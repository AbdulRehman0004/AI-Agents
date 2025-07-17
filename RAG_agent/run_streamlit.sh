#!/bin/bash
"""
Launcher script for the RAG Streamlit application
"""

echo "🚀 Starting RAG Document Query System..."
echo "📝 Make sure you have installed the requirements:"
echo "   pip install -r requirements.txt"
echo ""
echo "🔑 Ensure your OpenAI API key is set in config.py"
echo ""
echo "🌐 The app will open in your default browser"
echo "   If not, go to: http://localhost:8501"
echo ""

# Run the Streamlit app
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
