# ==========================================================
# CONFUSION MATRIX – Proposed Hybrid SVM+DBRT
# - Percentage format
# - Professional typography
# - Publication ready (PDF output)
# ==========================================================

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import joblib
import pandas as pd

# -----------------------------
# Typography & Aesthetic Setup
# -----------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
})

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "test.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "stacked_meta_model.pkl")
OUTPUT_DIR = os.path.join(BASE_DIR, "experiments")

# Import model helpers
import sys
sys.path.append(BASE_DIR)
from pipeline.analyze_clause import bert_predict, svm_predict

# -----------------------------
# Load Data
# -----------------------------
print("Loading test data...")
df = pd.read_csv(DATA_PATH)

X_test = df["clause_text"].values
y_true = df["label"].values

labels = sorted(list(set(y_true)))

# -----------------------------
# Load Model
# -----------------------------
print("Loading OOF Hybrid model...")
meta_model = joblib.load(MODEL_PATH)

# -----------------------------
# Generate Predictions
# -----------------------------
print("Generating predictions...")

y_pred = []

for clause in X_test:

    _, bert_probs = bert_predict(clause)
    _, svm_probs = svm_predict(clause)

    combined = np.concatenate([bert_probs, svm_probs]).reshape(1, -1)
    pred = meta_model.predict(combined)[0]
    y_pred.append(pred)

# -----------------------------
# Compute Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_true, y_pred, labels=labels)

# Convert to percentage
cm_percentage = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] * 100
cm_percentage = np.nan_to_num(cm_percentage)

# -----------------------------
# Plot Confusion Matrix
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(cm_percentage)

# Remove grid
ax.grid(False)

# Tick marks
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))

ax.set_xticklabels(labels, rotation=90)
ax.set_yticklabels(labels)

ax.set_xlabel("Predicted Label", fontweight="bold")
ax.set_ylabel("True Label", fontweight="bold")
ax.set_title("Confusion Matrix – Proposed Hybrid SVM+DBRT", fontweight="bold")

# Remove top/right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Add percentage text (no decimals)
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(
            j, i,
            f"{int(round(cm_percentage[i, j]))}%",
            ha="center",
            va="center",
            color="black",
            fontsize=7
        )

# Colorbar
cbar = fig.colorbar(im, ax=ax)
cbar.set_label("Percentage (%)", rotation=270, labelpad=15)

# Save
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

save_path = os.path.join(OUTPUT_DIR, "professional_confusion_matrix_hybrid.pdf")
plt.savefig(save_path)
plt.close()

print("Professional confusion matrix generated successfully.")
print("Saved to:", save_path)