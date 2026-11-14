import os
import re
import fitz
import docx

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        # Open the PDF
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    """Extracts text from a Word document."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text_from_txt(file_path):
    """Extracts text from a plain text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""

def clean_extracted_text(raw_text):
    """
    Removes HTML, weird spacing, and formatting artifacts.
    """
    if not raw_text:
        return ""
    
    # 1. Remove HTML tags (just in case)
    text = re.sub(r'<[^>]+>', '', raw_text)
    
    # 2. Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # 3. Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # 4. Strip leading/trailing whitespace
    return text.strip()

def process_file(file_path):
    """Main function to route the file to the correct extractor."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        raw_text = extract_text_from_docx(file_path)
    elif ext == '.txt':
        raw_text = extract_text_from_txt(file_path)
    else:
        return None # Unsupported format
        
    return clean_extracted_text(raw_text)