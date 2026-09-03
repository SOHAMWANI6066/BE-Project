"""
Hybrid Decision Controller (v6 - Confidence Gated Weighted Fusion)

True probability-level ensemble:
1) Confidence routing
2) Weighted probability fusion
3) ILCL correction
"""

from typing import Dict, List
import numpy as np
from .label_correction import apply_label_correction


# ==========================================================
# CONFIGURATION
# ==========================================================

ALPHA = 0.70  # 70% BERT, 30% SVM
HIGH_CONF_THRESHOLD = 0.80
LOW_CONF_THRESHOLD = 0.45
MARGIN_THRESHOLD = 0.20


# ==========================================================
# Helper
# ==========================================================

def get_margin(probs: np.ndarray) -> float:
    sorted_probs = np.sort(probs)
    return float(sorted_probs[-1] - sorted_probs[-2])


# ==========================================================
# Hybrid Predictor
# ==========================================================

def hybrid_predict(
    clause: str,
    bert_label: str,
    bert_probabilities: List[float],
    svm_label: str,
    svm_probabilities: List[float]
) -> Dict:

    bert_probs = np.array(bert_probabilities)
    svm_probs = np.array(svm_probabilities)

    if bert_probs.shape != svm_probs.shape:
        raise ValueError("Probability dimension mismatch")

    bert_conf = float(np.max(bert_probs))
    svm_conf = float(np.max(svm_probs))
    bert_margin = get_margin(bert_probs)

    # ======================================================
    # CONFIDENCE ROUTING
    # ======================================================

    # 1️⃣ Very High BERT Confidence → trust BERT
    if bert_conf >= HIGH_CONF_THRESHOLD:
        final_probs = bert_probs
        used_model = "BERT (High Confidence)"

    # 2️⃣ Very Low BERT Confidence → trust SVM
    elif bert_conf <= LOW_CONF_THRESHOLD:
        final_probs = svm_probs
        used_model = "SVM (Low BERT Confidence)"

    # 3️⃣ Strong margin → trust BERT
    elif bert_margin >= MARGIN_THRESHOLD:
        final_probs = bert_probs
        used_model = "BERT (Strong Margin)"

    # 4️⃣ Uncertain Zone → Weighted Fusion
    else:
        final_probs = (ALPHA * bert_probs) + ((1 - ALPHA) * svm_probs)
        used_model = "Weighted Fusion"

    # ======================================================
    # FINAL PREDICTION INDEX
    # ======================================================

    pred_id = int(np.argmax(final_probs))

    # ILCL is applied AFTER label mapping in analyze_clause
    # Here we return index only

    return {
        "pred_id": pred_id,
        "used_model": used_model,
        "bert_confidence": round(bert_conf, 4),
        "svm_confidence": round(svm_conf, 4),
        "fusion_confidence": round(float(np.max(final_probs)), 4),
        "bert_margin": round(bert_margin, 4),
        "clause_length": len(clause.split())
    }