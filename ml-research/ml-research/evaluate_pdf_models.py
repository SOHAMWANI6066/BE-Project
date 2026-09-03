# ==========================================================
# PDF MODEL COMPARISON SCRIPT
# - Runs BERT, SVM, and Hybrid side-by-side
# - Helps analyze real-world decision quality
# ==========================================================

import os
import sys
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = CURRENT_DIR
sys.path.append(PROJECT_ROOT)

from pipeline.analyze_clause import bert_predict, svm_predict
from hybrid.hybrid_predictor import hybrid_predict
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast
import joblib
import torch

# ---------------------------------------------
# LOAD MODELS
# ---------------------------------------------

print("Loading models...")

BASE_DIR = PROJECT_ROOT

SVM_MODEL_PATH = os.path.join(BASE_DIR, "models", "svm_final.pkl")
BERT_MODEL_PATH = os.path.join(BASE_DIR, "models", "distilbert_final")

svm_bundle = joblib.load(SVM_MODEL_PATH)
svm_vectorizer = svm_bundle["vectorizer"]
svm_model = svm_bundle["model"]

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = DistilBertTokenizerFast.from_pretrained(BERT_MODEL_PATH)
bert_model = DistilBertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
bert_model.to(DEVICE)
bert_model.eval()

print("Models loaded.\n")


# ---------------------------------------------
# HELPERS
# ---------------------------------------------

def bert_predict_local(clause):
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

    return label, probs


def svm_predict_local(clause):
    feats = svm_vectorizer.transform([clause])
    probs = svm_model.predict_proba(feats)[0]
    pred_id = int(np.argmax(probs))
    label = svm_model.classes_[pred_id]

    return label, probs


# ---------------------------------------------
# TEST ON SAMPLE CLAUSES
# ---------------------------------------------

def compare_clause(clause):

    print("\n====================================================")
    print("CLAUSE:")
    print(clause[:250], "...\n")

    # BERT
    bert_label, bert_probs = bert_predict_local(clause)
    bert_conf = float(np.max(bert_probs))

    # SVM
    svm_label, svm_probs = svm_predict_local(clause)
    svm_conf = float(np.max(svm_probs))

    # Hybrid
    hybrid_result = hybrid_predict(
        clause=clause,
        bert_label=bert_label,
        bert_probabilities=bert_probs,
        svm_label=svm_label,
        svm_probabilities=svm_probs
    )

    pred_id = hybrid_result["pred_id"]
    hybrid_label = bert_model.config.id2label[pred_id]

    print("BERT   :", bert_label, "| Conf:", round(bert_conf, 4))
    print("SVM    :", svm_label, "| Conf:", round(svm_conf, 4))
    print("HYBRID :", hybrid_label, "| Used:", hybrid_result["used_model"])
    print("Fusion Confidence:", hybrid_result["fusion_confidence"])
    print("====================================================\n")


# ---------------------------------------------
# MANUAL TEST (replace with extracted clauses)
# ---------------------------------------------

sample_clauses = [
    "The agreement may be terminated by either party upon thirty days written notice.",
    "Licensee shall not transfer this agreement without prior written consent.",
    "The liability of the supplier shall not exceed the fees paid under this agreement."
]

for clause in sample_clauses:
    compare_clause(clause)
