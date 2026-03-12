"""
Configuration file for the RAG system
"""
import os
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

# Set OpenAI API key
openai_key = os.getenv("OPENAI_API_KEY", "Please enter your OpenAI API key here")

# Verify API key is set
if not openai_key or openai_key == "Please enter your OpenAI API key here":
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable or update config.py with your key.")

# Initialize embeddings settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Database configuration
DB_PATH = "./db"
COLLECTION_NAME = "documents"
EMBEDDING_MODEL = "text-embedding-3-large"
