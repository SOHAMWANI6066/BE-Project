import fitz  # pip install pymupdf

def extract_clauses_from_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    # Simple clause split (improve later if needed)
    clauses = [c.strip() for c in full_text.split("\n") if len(c.strip()) > 30]

    return clauses
