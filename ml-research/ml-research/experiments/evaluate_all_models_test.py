
import os
import json
import time
import pandas as pd
import numpy as np
import joblib
import torch

from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from sklearn.preprocessing import label_binarize
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Hybrid import
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from pipeline.analyze_clause import analyze_clause


# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "test.csv")
SVM_MODEL_PATH = os.path.join(BASE_DIR, "models", "svm_final.pkl")
BERT_MODEL_PATH = os.path.join(BASE_DIR, "models", "distilbert_final")
OUTPUT_PATH = os.path.join(BASE_DIR, "metrics", "test_set_comparison.json")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --------------------------------------------------
# LOAD TEST DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)
y_true = df["label"].tolist()
clauses = df["clause_text"].tolist()


# --------------------------------------------------
# METRIC FUNCTION
# --------------------------------------------------

def compute_metrics(y_true, y_pred, start_time, end_time):
    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro",zero_division=0
    )

    unique_labels = sorted(list(set(y_true)))
    y_true_bin = label_binarize(y_true, classes=unique_labels)
    y_pred_bin = label_binarize(y_pred, classes=unique_labels)

    try:
        roc_auc = roc_auc_score(y_true_bin, y_pred_bin, average="macro")
    except:
        roc_auc = 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "inference_time_sec": round(end_time - start_time, 2)
    }


results = {}

# ==================================================
# 1️⃣ SVM TEST EVALUATION
# ==================================================

print("Evaluating SVM on Test Set...")

svm_bundle = joblib.load(SVM_MODEL_PATH)
vectorizer = svm_bundle["vectorizer"]
svm_model = svm_bundle["model"]

start = time.time()

X_features = vectorizer.transform(clauses)
svm_preds = svm_model.predict(X_features)

end = time.time()

results["SVM"] = compute_metrics(y_true, svm_preds, start, end)


# ==================================================
# 2️⃣ DISTILBERT TEST EVALUATION
# ==================================================

print("Evaluating DistilBERT on Test Set...")

tokenizer = DistilBertTokenizerFast.from_pretrained(BERT_MODEL_PATH)
bert_model = DistilBertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
bert_model.to(DEVICE)
bert_model.eval()

bert_preds = []

start = time.time()

for clause in clauses:
    inputs = tokenizer(
        clause,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    ).to(DEVICE)

    with torch.no_grad():
        outputs = bert_model(**inputs)

    logits = outputs.logits
    pred_id = torch.argmax(logits, dim=1).item()
    label = bert_model.config.id2label[pred_id]
    bert_preds.append(label)

end = time.time()

results["DistilBERT"] = compute_metrics(y_true, bert_preds, start, end)


# ==================================================
# 3️⃣ HYBRID TEST EVALUATION
# ==================================================

print("Evaluating Hybrid Model on Test Set...")

hybrid_preds = []

start = time.time()

for clause in clauses:
    result = analyze_clause(clause)
    hybrid_preds.append(result["clause_type"])

end = time.time()

results["Hybrid"] = compute_metrics(y_true, hybrid_preds, start, end)


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=4)

print("\nTest Set Evaluation Completed.")
print(json.dumps(results, indent=4))