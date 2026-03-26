import pdfplumber

def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file. Returns (text, error)."""
    try:
        pdf = pdfplumber.open(uploaded_file)
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        pdf.close()
        if not text.strip():
            return None, "PDF contains no extractable text (may be scanned/image-based)"
        return text[:3000], None  # truncate to 3000 chars to manage token limits
    except Exception as e:
        return None, f"Could not read PDF: {str(e)}"
