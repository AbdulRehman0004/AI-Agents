"""
Query engine for retrieving information from the vector database
"""
from database import initialize_database

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

def get_similar_documents(question, index, k=3):
    """Get similar documents without generating an answer.
    
    Args:
        question (str): The question to ask
        index: Vector database index
        k (int): Number of similar documents to retrieve
        
    Returns:
        list: List of similar document chunks
    """
    try:
        # Create retriever
        retriever = index.as_retriever(similarity_top_k=k)
        
        # Retrieve similar documents
        nodes = retriever.retrieve(question)
        
        return [{"text": node.text, "score": node.score} for node in nodes]
        
    except Exception as e:
        return f"❌ Error retrieving documents: {str(e)}"

def batch_query(questions, index, k=3):
    """Process multiple queries at once.
    
    Args:
        questions (list): List of questions to ask
        index: Vector database index
        k (int): Number of similar documents to retrieve
        
    Returns:
        list: List of answers corresponding to each question
    """
    results = []
    for question in questions:
        answer = query_database(question, index, k)
        results.append({"question": question, "answer": answer})
    
    return results
