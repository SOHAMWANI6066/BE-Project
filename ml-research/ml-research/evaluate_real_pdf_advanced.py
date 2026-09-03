# ==========================================================
# REAL PDF ADVANCED EVALUATION
# - Arbitration statistics
# - Confidence comparison
# - Usage distribution
# - Saves JSON for research charts
# ==========================================================

import os
import sys
import json
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = CURRENT_DIR
sys.path.append(PROJECT_ROOT)

from pipeline.analyze_clause import bert_predict, svm_predict, analyze_clause
from pipeline.pdf_extractor import extract_clauses_from_pdf

PDF_FOLDER = os.path.join(PROJECT_ROOT, "data", "test_pdfs")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "metrics", "real_world_evaluation.json")

total_clauses = 0
disagreements = 0

bert_conf_total = 0
svm_conf_total = 0
hybrid_conf_total = 0

# 🔥 MUST MATCH EXACT STRINGS FROM hybrid_predictor.py
routing_stats = {
    "BERT (High Confidence)": 0,
    "BERT (Strong Margin)": 0,
    "SVM (Low BERT Confidence)": 0,
    "Weighted Fusion": 0
}

print("\nRunning advanced PDF evaluation...\n")

for filename in os.listdir(PDF_FOLDER):

    if not filename.endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)
    clauses = extract_clauses_from_pdf(pdf_path)

    for clause in clauses:

        total_clauses += 1

        bert_label, bert_probs = bert_predict(clause)
        svm_label, svm_probs = svm_predict(clause)
        hybrid_result = analyze_clause(clause)

        hybrid_label = hybrid_result["clause_type"]
        used_model = hybrid_result["decision_trace"]["classification_used"]

        # -------------------------
        # Disagreement Tracking
        # -------------------------
        if bert_label != svm_label:
            disagreements += 1

        # -------------------------
        # Confidence Aggregation
        # -------------------------
        bert_conf_total += hybrid_result["decision_trace"]["bert_confidence"]
        svm_conf_total += hybrid_result["decision_trace"]["svm_confidence"]
        hybrid_conf_total += hybrid_result["decision_trace"]["fusion_confidence"]

        # -------------------------
        # Routing Statistics
        # -------------------------
        if used_model in routing_stats:
            routing_stats[used_model] += 1

# -------------------------------
# FINAL STATISTICS
# -------------------------------

results = {
    "total_clauses": total_clauses,
    "bert_svm_disagreements": disagreements,
    "disagreement_rate_percent": round((disagreements / total_clauses) * 100, 2),

    "average_bert_confidence": round(bert_conf_total / total_clauses, 4),
    "average_svm_confidence": round(svm_conf_total / total_clauses, 4),
    "average_hybrid_confidence": round(hybrid_conf_total / total_clauses, 4),

    "routing_distribution_percent": {
        key: round((value / total_clauses) * 100, 2)
        for key, value in routing_stats.items()
    }
}

os.makedirs(os.path.join(PROJECT_ROOT, "metrics"), exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=4)

print("\nAdvanced Real-World Evaluation Results:")
print(json.dumps(results, indent=4))
print(f"\nSaved to → {OUTPUT_PATH}")
