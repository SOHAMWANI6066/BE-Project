import os
from pipeline.pdf_extractor import extract_clauses_from_pdf
from pipeline.analyze_clause import analyze_clause

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(CURRENT_DIR, "data", "test_pdfs")


print("Scanning PDF folder...\n")

for file in os.listdir(PDF_FOLDER):

    if not file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, file)

    print("\n" + "="*80)
    print(f"📄 PROCESSING FILE: {file}")
    print("="*80)

    clauses = extract_clauses_from_pdf(pdf_path)
    print(f"Total clauses extracted: {len(clauses)}")

    for i, clause in enumerate(clauses[:20]):  # limit first 20 per file

        result = analyze_clause(clause)

        print("\n" + "-"*60)
        print(f"CLAUSE {i+1}")
        print(clause[:100], "...\n")

        print("Predicted:", result["clause_type"])
        print("Used:", result["decision_trace"]["classification_used"])
        print("Confidence:", result["decision_trace"]["fusion_confidence"])
