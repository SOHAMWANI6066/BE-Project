import json
import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Typography & Aesthetic Setup
# -----------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
})

# -----------------------------
# Colors (UNCHANGED)
# -----------------------------
COLORS = ['#4477AA', '#EE6677', '#228833']
HATCHES = ['//', '\\\\', 'xx']

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS_DIR = os.path.join(BASE_DIR, "metrics")
OUTPUT_DIR = os.path.join(BASE_DIR, "experiments")

# -----------------------------
# Load JSON Data (Learning Curve)
# -----------------------------
def load_data():
    files = {
        "SVM": "svm_learning_curve.json",
        "DistilBERT": "distilbert_learning_curve.json",
        "Hybrid": "hybrid_learning_curve.json"   # IMPORTANT: must be learning curve file
    }

    data = {}

    for model, filename in files.items():
        path = os.path.join(METRICS_DIR, filename)
        with open(path, "r") as f:
            data[model] = json.load(f)

    # Learning curve expects numeric keys like "40", "50", etc.
    splits = sorted([int(k) for k in data["SVM"].keys()])
    return data, splits


DATA, SPLITS = load_data()

# -----------------------------
# Plot Function
# -----------------------------
def plot_percentage_bar(metric_name, filename):

    labels = ["SVM", "DistilBERT", "Hybrid"]

    metric_display_names = {
        "accuracy": "Accuracy (%)",
        "precision": "Precision (%)",
        "recall": "Recall (%)",
        "f1_score": "F1-Score (%)"
    }

    clean_metric = metric_display_names.get(metric_name, metric_name)

    x = np.arange(len(SPLITS))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 6))

    for i, label in enumerate(labels):

        values = [
            DATA[label][str(split)][metric_name] * 100
            for split in SPLITS
        ]

        bars = ax.bar(
            x + (i - 1) * width,
            values,
            width,
            label="Proposed Hybrid SVM+DBRT" if label == "Hybrid" else label,
            color=COLORS[i],
            edgecolor='black',
            linewidth=1.2
        )

    ax.set_ylabel(clean_metric, fontweight="bold")
    ax.set_xlabel("Training Data Percentage (%)", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([f"{split}%" for split in SPLITS])

    ax.set_ylim(0, 100)

    # Remove background grid
    ax.grid(False)

    # Clean spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=3,
        frameon=False
    )

    plt.subplots_adjust(bottom=0.22)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path)
    plt.close()


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":

    metrics = ["accuracy", "precision", "recall", "f1_score"]

    for metric in metrics:
        plot_percentage_bar(
            metric,
            f"professional_{metric}_comparison.png"
        )

    print("All 4 professional percentage charts generated successfully.")