# ==========================================================
# REAL-TIME PERFORMANCE METRICS
# Proposed Hybrid SVM+DBRT
# Clean Academic Single-Color Version
# ==========================================================

import os
import matplotlib.pyplot as plt

# -----------------------------
# Typography Setup (IEEE style)
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
# Your OOF Hybrid Results
# -----------------------------
accuracy = 0.7589
precision = 0.7192
recall = 0.6553
f1 = 0.6608

metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
values = [
    int(round(accuracy * 100)),
    int(round(precision * 100)),
    int(round(recall * 100)),
    int(round(f1 * 100)),
]

# Professional academic blue
bar_color = "#1f4e79"

# -----------------------------
# Plot
# -----------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.5))

bars = ax.bar(
    metrics,
    values,
    color=bar_color,
    edgecolor="black",
    linewidth=1.2
)

ax.set_ylim(0, 100)
ax.set_ylabel("Percentage (%)", fontweight="bold")
ax.set_title("Real-Time Clause Classification Performance\n(Proposed Hybrid SVM+DBRT)",
             fontweight="bold", pad=10)

# Remove grid and extra spines
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Add percentage labels
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 2,
        f"{int(height)}%",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold"
    )

# -----------------------------
# Save as PDF
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "hybrid_realtime_metrics.png")

plt.savefig(OUTPUT_PATH)
plt.close()

print("Professional real-time performance chart generated.")
print("Saved to:", OUTPUT_PATH)