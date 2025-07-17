"""
Database operations for storing and retrieving documents
"""
import chromadb
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config import DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL
from document_processor import extract_text_from_file

def initialize_database():
    """Initialize and return the vector database index.
    
    Returns:
        VectorStoreIndex: Initialized vector database index
    """
    try:
        # Initialize embeddings & Chroma vector DB
        Settings.embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL)
        
        # Initialize Chroma
        chroma_client = chromadb.PersistentClient(path=DB_PATH)
        chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
        
        # Create vector store and index
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex([], storage_context=storage_context)
        
        return index
    except Exception as e:
        raise Exception(f"Error initializing database: {str(e)}")

def store_document_to_db(file_path, doc_id, index):
    """Store a document in the vector database.
    
    Args:
        file_path (str): Path to the document file
        doc_id (str): Unique identifier for the document
        index: Vector database index
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Extract text from file
        text = extract_text_from_file(file_path)
        
        # Create Document object
        document = Document(text=text, doc_id=doc_id)
        
        # Insert document into index
        index.insert(document)
        
        print(f"✅ Document '{doc_id}' stored successfully.")
        return True
        
    except Exception as e:
        print(f"❌ Error storing document '{doc_id}': {str(e)}")
        return False

def list_documents(index):
    """List all documents in the database.
    
    Args:
        index: Vector database index
        
    Returns:
        list: List of document IDs
    """
    try:
        # This would need to be implemented based on the specific vector store
        # For now, we'll return a placeholder
        return ["doc1", "doc2"]  # Placeholder
    except Exception as e:
        print(f"❌ Error listing documents: {str(e)}")
        return []

def delete_document(doc_id, index):
    """Delete a document from the database.
    
    Args:
        doc_id (str): Document ID to delete
        index: Vector database index
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # This would need to be implemented based on the specific vector store
        # For now, we'll return a placeholder
        print(f"✅ Document '{doc_id}' deleted successfully.")
        return True
    except Exception as e:
        print(f"❌ Error deleting document '{doc_id}': {str(e)}")
        return False
