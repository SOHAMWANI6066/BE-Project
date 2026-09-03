
"""
End-to-End Clause Analysis
Confidence-Gated Weighted Hybrid (BERT + Calibrated SVM)
"""

import os
import torch
import joblib
import numpy as np

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

# ---- Internal modules ----
from hybrid.hybrid_predictor import hybrid_predict
from hybrid.label_correction import apply_label_correction
from risk.risk_mapping import get_clause_risk
from simplification.simplifier import simplify_clause
from post_processing.classification_hardening import harden_classification


# ==========================================================
# ABSOLUTE PATH FIX
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SVM_MODEL_PATH = os.path.join(BASE_DIR, "models", "svm_final.pkl")
BERT_MODEL_PATH = os.path.join(BASE_DIR, "models", "distilbert_final")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ==========================================================
# LOAD MODELS (LOAD ONCE)
# ==========================================================

print("Loading ML models...")

svm_bundle = joblib.load(SVM_MODEL_PATH)
svm_vectorizer = svm_bundle["vectorizer"]
svm_model = svm_bundle["model"]

tokenizer = DistilBertTokenizerFast.from_pretrained(BERT_MODEL_PATH)
bert_model = DistilBertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
bert_model.to(DEVICE)
bert_model.eval()

print("Models loaded successfully.")


# ==========================================================
# MODEL HELPERS
# ==========================================================

def bert_predict(clause: str):
    inputs = tokenizer(
        clause,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = bert_model(**inputs)

    logits = outputs.logits.squeeze().cpu().numpy()
    probs = torch.softmax(torch.tensor(logits), dim=0).numpy()

    pred_id = int(np.argmax(probs))
    label = bert_model.config.id2label[pred_id]

    return label, probs.tolist()


def svm_predict(clause: str):
    feats = svm_vectorizer.transform([clause])

    # Calibrated SVM supports probability
    probs = svm_model.predict_proba(feats)[0]
    pred_id = int(np.argmax(probs))
    label = svm_model.classes_[pred_id]

    return label, probs.tolist()


# ==========================================================
# PUBLIC PIPELINE FUNCTION
# ==========================================================

def analyze_clause(clause: str) -> dict:

    # ------------------------------------------------------
    # 1️⃣ Base Model Predictions
    # ------------------------------------------------------
    bert_label, bert_probs = bert_predict(clause)
    svm_label, svm_probs = svm_predict(clause)

    # ------------------------------------------------------
    # 2️⃣ Hybrid Probability Fusion
    # ------------------------------------------------------
    hybrid_result = hybrid_predict(
        clause=clause,
        bert_label=bert_label,
        bert_probabilities=bert_probs,
        svm_label=svm_label,
        svm_probabilities=svm_probs
    )

    # ------------------------------------------------------
    # 3️⃣ Convert pred_id → Label Name (CRITICAL FIX)
    # ------------------------------------------------------
    pred_id = hybrid_result["pred_id"]
    raw_label = bert_model.config.id2label[pred_id]

    # ------------------------------------------------------
    # 4️⃣ Intelligent Label Correction Layer (ILCL)
    # ------------------------------------------------------
    corrected_label = apply_label_correction(clause, raw_label)

    # ------------------------------------------------------
    # 5️⃣ Hardening Layer
    # ------------------------------------------------------
    clause_type = harden_classification(clause, corrected_label)

# ------------------------------------------------------
    # 6️⃣ Risk Mapping
    # ------------------------------------------------------
    risk_level = get_clause_risk(clause_type)

    # ------------------------------------------------------
    # 7️⃣ Simplification (Safe Execution)
    # ------------------------------------------------------
    try:
        simplification = simplify_clause(
            clause_text=clause,
            clause_type=clause_type
        )
        simplified_text = simplification.get("simplified_text")
        method = simplification.get("method")
    except Exception:
        simplified_text = None
        method = "error"

    # ------------------------------------------------------
    # 8️⃣ Final Structured Output
    # ------------------------------------------------------
    return {
        "original_clause": clause,
        "clause_type": clause_type,
        "risk_level": risk_level,
        "simplified_text": simplified_text,
        "simplification_method": method,
        "decision_trace": {
            "classification_used": hybrid_result.get("used_model"),
            "bert_confidence": hybrid_result.get("bert_confidence"),
            "svm_confidence": hybrid_result.get("svm_confidence"),
            "fusion_confidence": hybrid_result.get("fusion_confidence"),
            "bert_margin": hybrid_result.get("bert_margin"),
            "clause_length": hybrid_result.get("clause_length")
        }
    }


# ==========================================================
# CLI TEST
# ==========================================================

if __name__ == "__main__":

    test_clause = (
        "The agreement may be terminated by either party with thirty days "
        "prior written notice in the event of a material breach."
    )

    result = analyze_clause(test_clause)

    print("\nCLAUSE ANALYSIS RESULT\n")
    for k, v in result.items():
        print(f"{k}: {v}")