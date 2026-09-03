# ==========================================================
# CLASS DISTRIBUTION PLOT (Clean IEEE Style)
# - Large value labels
# - No grid
# - White background
# - Publication ready
# ==========================================================

import os
import matplotlib.pyplot as plt

# -----------------------------
# Typography Setup
# -----------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 12,
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
})

# -----------------------------
# Example Values (replace with yours)
# -----------------------------
labels = ["SVM", "DistilBERT", "Proposed Hybrid\nSVM+DBRT"]
values = [67, 70, 76]   # percentages

# Professional color emphasis
colors = ["#B0B0B0", "#808080", "#000000"]

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.5))

bars = ax.bar(
    labels,
    values,
    color=colors,
    edgecolor="black",
    linewidth=1.2
)

ax.set_ylabel("Accuracy (%)", fontweight="bold")
ax.set_ylim(0, 100)

# Remove grid and extra spines
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Add large value labels
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 2,
        f"{int(height)}%",
        ha="center",
        va="bottom",
        fontsize=13,
        fontweight="bold"
    )

ax.set_title("Test Set Accuracy Comparison", fontweight="bold", pad=10)

# -----------------------------
# Save
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "final_accuracy_distribution.pdf")

plt.savefig(OUTPUT_PATH)
plt.close()

print("Professional distribution chart generated.")
print("Saved to:", OUTPUT_PATH)