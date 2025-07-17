"""
Utility functions for the RAG system
"""
import os
from pathlib import Path

def validate_file_path(file_path):
    """Validate if a file path exists and is readable.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        path = Path(file_path)
        return path.exists() and path.is_file()
    except Exception:
        return False

def get_file_size(file_path):
    """Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        int: File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0

def format_file_size(size_bytes):
    """Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/1024**2:.1f} MB"
    else:
        return f"{size_bytes/1024**3:.1f} GB"

def list_supported_files(directory):
    """List all supported files in a directory.
    
    Args:
        directory (str): Directory path
        
    Returns:
        list: List of supported file paths
    """
    supported_extensions = ['.pdf', '.html']
    files = []
    
    try:
        for file_path in Path(directory).rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                files.append(str(file_path))
    except Exception as e:
        print(f"Error listing files: {str(e)}")
    
    return files

def clean_text(text):
    """Clean and normalize text content.
    
    Args:
        text (str): Raw text content
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove common artifacts
    text = text.replace('\x00', '')  # Remove null characters
    text = text.replace('\ufeff', '')  # Remove BOM
    
    return text.strip()

def generate_doc_id(file_path):
    """Generate a unique document ID from file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Generated document ID
    """
    import hashlib
    
    # Use file path and modification time for uniqueness
    try:
        mtime = os.path.getmtime(file_path)
        content = f"{file_path}_{mtime}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    except Exception:
        # Fallback to just the filename
        return Path(file_path).stem
