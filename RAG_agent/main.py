"""
Main application file that demonstrates the RAG system
"""
from database import initialize_database, store_document_to_db
from query_engine import query_database, batch_query
from config import openai_key

def main():
    """Main function to demonstrate the RAG system."""
    print("🚀 Starting RAG System...")
    print(f"🔑 OpenAI API Key: {'Set' if openai_key else 'Not set'}")
    
    # Initialize database
    print("\n🔄 Initializing database...")
    try:
        index = initialize_database()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize database: {str(e)}")
        return
    
    # Store documents
    print("\n📄 Storing documents...")
    documents = [
        ("english-ausco-australian-law.pdf", "doc1"),
        ("2023_Australian_Constitution.pdf", "doc2")
    ]
    
    for file_path, doc_id in documents:
        store_document_to_db(file_path, doc_id, index)
    
    # Single query
    print("\n❓ Querying database...")
    question = "What is the main purpose of the document?"
    answer = query_database(question, index, k=3)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    
    # Batch queries
    print("\n📋 Batch querying...")
    questions = [
        "What are the key provisions mentioned?",
        "Who are the main stakeholders?",
        "What are the important dates mentioned?"
    ]
    
    results = batch_query(questions, index, k=3)
    for result in results:
        print(f"\nQ: {result['question']}")
        print(f"A: {result['answer']}")

def interactive_mode():
    """Interactive mode for querying the database."""
    print("🔄 Initializing database for interactive mode...")
    index = initialize_database()
    print("✅ Database ready! Type 'quit' to exit.\n")
    
    while True:
        question = input("Ask a question: ")
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        answer = query_database(question, index, k=3)
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()
