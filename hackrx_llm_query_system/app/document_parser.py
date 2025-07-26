# app/document_parser.py
import requests
import tempfile
import pdfplumber
import docx
import re

def download_file(url):
    response = requests.get(url)
    tf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    tf.write(response.content)
    tf.close()
    return tf.name

def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    sections = []
    # Split by heading pattern, e.g., Clause 1, Section II, etc.
    pattern = re.compile(r"((Section|Clause|Article|Part)\s+\d+[\.\:]?.*)", re.IGNORECASE)
    raw = re.split(pattern, text)
    # Merge split parts: [text, header, text, header, ...]
    for i in range(1, len(raw), 2):
        sections.append({
            "clause_id": raw[i].strip(),
            "text": (raw[i+1] if i+1 < len(raw) else "").strip()
        })
    return sections

def parse_docx(file_path):
    doc = docx.Document(file_path)
    data = ""
    for para in doc.paragraphs:
        data += para.text + "\n"
    # Use same pattern as PDF
    return parse_pdf(data)

def parse_documents_from_blob_url(url):
    file_path = download_file(url)
    if url.lower().endswith('.pdf'):
        return parse_pdf(file_path)
    elif url.lower().endswith('.docx'):
        return parse_docx(file_path)
    else:
        raise Exception("Unsupported file type. Only PDF & DOCX supported.")
