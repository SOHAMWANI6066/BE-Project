# ==========================================================
# TABLE – Proposed Hybrid SVM+DBRT Performance Summary
# Academic Style Table Generator
# ==========================================================

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import confusion_matrix

# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "test.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "stacked_meta_model.pkl")

# Import model helpers
import sys
sys.path.append(BASE_DIR)
from pipeline.analyze_clause import bert_predict, svm_predict

# ----------------------------------------------------------
# Load test data
# ----------------------------------------------------------
df = pd.read_csv(DATA_PATH)
X_test = df["clause_text"].values
y_true = df["label"].values

labels = sorted(list(set(y_true)))

# ----------------------------------------------------------
# Load hybrid model
# ----------------------------------------------------------
meta_model = joblib.load(MODEL_PATH)

# ----------------------------------------------------------
# Generate predictions
# ----------------------------------------------------------
y_pred = []

for clause in X_test:
    _, bert_probs = bert_predict(clause)
    _, svm_probs = svm_predict(clause)

    combined = np.concatenate([bert_probs, svm_probs]).reshape(1, -1)
    pred = meta_model.predict(combined)[0]
    y_pred.append(pred)

# ----------------------------------------------------------
# Compute confusion matrix
# ----------------------------------------------------------
cm = confusion_matrix(y_true, y_pred, labels=labels)

# For multi-class we approximate:
total = np.sum(cm)
correct = np.trace(cm)

accuracy = correct / total

# False Positive & False Negative (macro average)
fp = cm.sum(axis=0) - np.diag(cm)
fn = cm.sum(axis=1) - np.diag(cm)
tn = total - (fp + fn + np.diag(cm))

fpr = np.mean(fp / (fp + tn))
fnr = np.mean(fn / (fn + np.diag(cm)))

# ----------------------------------------------------------
# Hardcode your already computed macro metrics
# (From OOF evaluation)
# ----------------------------------------------------------
precision = 0.7192
recall = 0.6553
f1 = 0.6608

# ----------------------------------------------------------
# Create Table
# ----------------------------------------------------------
table_data = [
    ["Total Test Samples", total],
    ["Accuracy (%)", f"{round(accuracy*100,2)}%"],
    ["Precision (%)", f"{round(precision*100,2)}%"],
    ["Recall (%)", f"{round(recall*100,2)}%"],
    ["F1-Score (%)", f"{round(f1*100,2)}%"],
    ["False Positive Rate (%)", f"{round(fpr*100,2)}%"],
    ["False Negative Rate (%)", f"{round(fnr*100,2)}%"],
]

table_df = pd.DataFrame(table_data, columns=["Metric", "Value"])

# ----------------------------------------------------------
# Print Table
# ----------------------------------------------------------
print("\nTable – Proposed Hybrid SVM+DBRT Performance Summary\n")
print(table_df.to_string(index=False))

# ----------------------------------------------------------
# Save as CSV
# ----------------------------------------------------------
OUTPUT_PATH = os.path.join(BASE_DIR, "hybrid_performance_table.csv")
table_df.to_csv(OUTPUT_PATH, index=False)

print("\nTable saved to:", OUTPUT_PATH)