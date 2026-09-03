import os
import sys
import json
import time
import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from sklearn.preprocessing import label_binarize

# --------------------------------------------------
# FIX PYTHON PATH (CRITICAL)
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from pipeline.analyze_clause import analyze_clause


# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_PATH = os.path.join(BASE_DIR, "metrics", "hybrid_learning_curve.json")

SPLITS = [40, 50, 60, 70, 80, 90, 100]


# --------------------------------------------------
# EVALUATION FUNCTION
# --------------------------------------------------

def evaluate_split(split_percent):
    file_path = os.path.join(DATA_DIR, f"train_{split_percent}.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    df = pd.read_csv(file_path)

    if "clause_text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'clause_text' and 'label' columns")

    y_true = []
    y_pred = []

    start_time = time.time()

    for _, row in df.iterrows():
        clause = str(row["clause_text"])
        true_label = str(row["label"])

        try:
            result = analyze_clause(clause)
            predicted_label = result["clause_type"]
        except Exception:
            predicted_label = "ERROR"

        y_true.append(true_label)
        y_pred.append(predicted_label)

    end_time = time.time()

    # -------------------------
    # METRICS
    # -------------------------

    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    # Multi-class ROC AUC
    unique_labels = sorted(list(set(y_true)))
    y_true_bin = label_binarize(y_true, classes=unique_labels)
    y_pred_bin = label_binarize(y_pred, classes=unique_labels)

    try:
        roc_auc = roc_auc_score(y_true_bin, y_pred_bin, average="macro")
    except:
        roc_auc = 0.0

    inference_time = round(end_time - start_time, 2)

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "inference_time_sec": inference_time
    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    results = {}

    print("\nStarting Hybrid Learning Curve Evaluation...\n")

    for split in SPLITS:
        print(f"Evaluating Hybrid Model on {split}% data...")
        metrics = evaluate_split(split)
        results[str(split)] = metrics

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print("\nHybrid learning curve saved successfully.")
    print(f"Saved at: {OUTPUT_PATH}")


# --------------------------------------------------
# SAFE ENTRY
# --------------------------------------------------

if __name__ == "__main__":
    main()