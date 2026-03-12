"""
Document processing utilities for extracting text from various file formats
"""
import fitz  # PyMuPDF
from bs4 import BeautifulSoup

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content
    """
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text("text") + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF file {pdf_path}: {str(e)}")
    
    return text

def extract_text_from_html(html_path):
    """Extract text from an HTML file.
    
    Args:
        html_path (str): Path to the HTML file
        
    Returns:
        str: Extracted text content
    """
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(separator="\n")
    except Exception as e:
        raise Exception(f"Error reading HTML file {html_path}: {str(e)}")

def extract_text_from_file(file_path):
    """Extract text from a file based on its extension.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Extracted text content
        
    Raises:
        ValueError: If file type is not supported
    """
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".html"):
        return extract_text_from_html(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}. Use PDF or HTML.")
