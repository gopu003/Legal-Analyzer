import pdfplumber
from docx import Document

def extract_text(path, file_type):
    if file_type == "pdf":
        with pdfplumber.open(path) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file_type == "docx":
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file type."
