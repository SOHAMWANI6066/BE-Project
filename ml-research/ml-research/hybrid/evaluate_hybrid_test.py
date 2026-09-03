# ==========================================================
# OOF STACKED HYBRID TEST SET EVALUATION
# - Uses frozen test.csv (20%)
# - Uses BERT + Calibrated SVM + OOF-trained Logistic meta model
# - 66-dim feature vector (no scaler)
# ==========================================================

import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ----------------------------------------------------------
# FIX PYTHON PATH
# ----------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from pipeline.analyze_clause import bert_predict, svm_predict

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "test.csv")
META_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "stacked_meta_model.pkl")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "metrics", "hybrid_final_metrics.json")

# ----------------------------------------------------------
# LOAD META MODEL
# ----------------------------------------------------------
print("📦 Loading OOF stacked meta-model...")
meta_model = joblib.load(META_MODEL_PATH)

# ----------------------------------------------------------
# LOAD TEST DATA
# ----------------------------------------------------------
print("📥 Loading test dataset...")
df = pd.read_csv(DATA_PATH)

X_test = df["clause_text"].values
y_true = df["label"].values

y_pred = []

print("🚀 Running OOF STACKED Hybrid inference on test set...")

start_time = time.time()

# ----------------------------------------------------------
# INFERENCE LOOP
# ----------------------------------------------------------
for clause in X_test:

    # 1️⃣ BERT probabilities (33)
    _, bert_probs = bert_predict(clause)
    bert_probs = np.array(bert_probs)

    # 2️⃣ SVM probabilities (33)
    _, svm_probs = svm_predict(clause)
    svm_probs = np.array(svm_probs)

    # 3️⃣ Combine → 66-dim feature
    combined_features = np.concatenate([bert_probs, svm_probs]).reshape(1, -1)

    # 4️⃣ Meta prediction
    final_label = meta_model.predict(combined_features)[0]

    y_pred.append(final_label)

end_time = time.time()
inference_time = round(end_time - start_time, 2)

# ----------------------------------------------------------
# METRICS
# ----------------------------------------------------------
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
recall = recall_score(y_true, y_pred, average="macro", zero_division=0)
f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

metrics = {
    "accuracy": round(accuracy, 4),
    "precision": round(precision, 4),
    "recall": round(recall, 4),
    "f1_score": round(f1, 4),
    "inference_time_sec": inference_time
}

# ----------------------------------------------------------
# SAVE RESULTS
# ----------------------------------------------------------
os.makedirs(os.path.join(PROJECT_ROOT, "metrics"), exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

print("\n📊 OOF STACKED Hybrid Test Metrics:")
print(metrics)
print(f"\n💾 Saved to → {OUTPUT_PATH}")