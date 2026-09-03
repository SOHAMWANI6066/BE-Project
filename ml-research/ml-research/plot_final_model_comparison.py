# ==========================================================
# FINAL MODEL COMPARISON (IEEE PUBLICATION STYLE)
# - SVM
# - DistilBERT
# - Proposed Hybrid SVM+DBRT
# - Percentage format (no decimals)
# ==========================================================

import os
import matplotlib.pyplot as plt

# -----------------------------
# Typography (IEEE Style)
# -----------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
})

# -----------------------------
# 🔹 Replace with your final test values if needed
# -----------------------------
svm_acc = 0.67
bert_acc = 0.70
hybrid_acc = 0.7589   # OOF Hybrid result

# Convert to percentage (NO floating points)
svm_pct = int(round(svm_acc * 100))
bert_pct = int(round(bert_acc * 100))
hybrid_pct = int(round(hybrid_acc * 100))

models = ["SVM", "DistilBERT", "Proposed Hybrid\nSVM+DBRT"]
accuracies = [svm_pct, bert_pct, hybrid_pct]

# Professional grayscale palette
colors = ["#4C4C4C", "#7F7F7F", "#000000"]

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.5))

bars = ax.bar(
    models,
    accuracies,
    color=colors,
    edgecolor="black",
    linewidth=1.2
)

ax.set_ylabel("Accuracy (%)", fontweight="bold")
ax.set_xlabel("Models", fontweight="bold")
ax.set_ylim(60, 85)

# Remove unnecessary spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Remove grid
ax.grid(False)

# Add percentage labels
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 1,
        f"{int(height)}%",
        ha="center",
        va="bottom",
        fontweight="bold"
    )

plt.title("Test Set Accuracy Comparison", fontweight="bold", pad=10)

# -----------------------------
# Save as IEEE-ready PDF
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "final_model_comparison_ieee.png")

plt.savefig(OUTPUT_PATH)
plt.close()

print("Professional IEEE-style comparison chart generated.")
print("Saved to:", OUTPUT_PATH)