import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import os
import chromadb
from openai import OpenAI

# Correct llama-index imports
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# Load OpenAI API key from config.py
try:
    from config import openai_key
    os.environ["OPENAI_API_KEY"] = openai_key
except ImportError:
    raise RuntimeError("Could not import openai_key from config.py. Please ensure it is set.")

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable or in config.py")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text("text") + "\n"
    return text

def extract_text_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup.get_text(separator="\n")

# Initialize embeddings settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

def initialize_database():
    """Initialize and return the vector database index."""
    # Initialize embeddings & Chroma vector DB
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    
    # Initialize Chroma
    chroma_client = chromadb.PersistentClient(path="./db")
    chroma_collection = chroma_client.get_or_create_collection("documents")
    
    # Create vector store and index
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)
    
    return index

def store_document_to_db(file_path, doc_id, index):
    """Store a document in the vector database.
    
    Args:
        file_path (str): Path to the document file
        doc_id (str): Unique identifier for the document
        index: Vector database index
    """
    try:
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".html"):
            text = extract_text_from_html(file_path)
        else:
            raise ValueError("Unsupported file type. Use PDF or HTML.")
        
        # Create Document object
        document = Document(text=text, doc_id=doc_id)
        
        # Insert document into index
        index.insert(document)
        
        print(f"✅ Document '{doc_id}' stored successfully.")
        return True
        
    except Exception as e:
        print(f"❌ Error storing document '{doc_id}': {str(e)}")
        return False

def query_database(question, index, k=3):
    """Query the vector database and return an answer.
    
    Args:
        question (str): The question to ask
        index: Vector database index
        k (int): Number of similar documents to retrieve
        
    Returns:
        str: The answer to the question
    """
    try:
        # Create query engine
        query_engine = index.as_query_engine(similarity_top_k=k)
        
        # Query the index
        response = query_engine.query(question)
        
        return str(response)
        
    except Exception as e:
        return f"❌ Error querying database: {str(e)}"

def main():
    """Main function to demonstrate the RAG system."""
    # Initialize database
    print("🔄 Initializing database...")
    index = initialize_database()
    
    # Store documents
    print("📄 Storing documents...")
    store_document_to_db("english-ausco-australian-law.pdf", "doc1", index)
    # store_document_to_db("example.html", "doc2", index)
    
    # Query the database
    print("❓ Querying database...")
    question = "What is the main purpose of the document?"
    answer = query_database(question, index, k=3)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()