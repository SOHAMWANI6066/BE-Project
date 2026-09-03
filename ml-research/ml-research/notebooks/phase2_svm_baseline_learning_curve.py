"""
PHASE 2 – MODEL 1
SVM Baseline with Learning Curve Charts
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score

# -----------------------------
# PATHS
# -----------------------------

BASE_DIR = "ml-research/data/processed"

TRAIN_FILES = {
    40: "train_40.csv",
    50: "train_50.csv",
    60: "train_60.csv",
    70: "train_70.csv",
    80: "train_80.csv",
    90: "train_90.csv",
    100: "train_100.csv",
}

TEST_FILE = "test.csv"

# -----------------------------
# LOAD TEST SET (FIXED)
# -----------------------------

test_df = pd.read_csv(f"{BASE_DIR}/{TEST_FILE}")

X_test = test_df["clause_text"]
y_test = test_df["label"]

# -----------------------------
# STORAGE FOR RESULTS
# -----------------------------

train_sizes = []
accuracies = []
f1_scores = []

# -----------------------------
# TRAIN & EVALUATE
# -----------------------------

for percent, filename in TRAIN_FILES.items():
    print(f"\n🔹 Training SVM with {percent}% training data")

    train_df = pd.read_csv(f"{BASE_DIR}/{filename}")

    X_train = train_df["clause_text"]
    y_train = train_df["label"]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2)
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Linear SVM
    svm = LinearSVC(random_state=42)
    svm.fit(X_train_vec, y_train)

    # Prediction
    y_pred = svm.predict(X_test_vec)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")

    train_sizes.append(percent)
    accuracies.append(acc)
    f1_scores.append(f1)

    print(f"Accuracy: {acc:.4f}")
    print(f"Macro F1: {f1:.4f}")

# -----------------------------
# SAVE RESULTS TABLE
# -----------------------------

results_df = pd.DataFrame({
    "Training_Size_%": train_sizes,
    "Accuracy": accuracies,
    "Macro_F1": f1_scores
})

results_path = f"{BASE_DIR}/svm_learning_curve_results.csv"
results_df.to_csv(results_path, index=False)

print(f"\n📁 Results saved to: {results_path}")

# -----------------------------
# PLOT LEARNING CURVE
# -----------------------------

plt.figure(figsize=(8, 5))
plt.plot(train_sizes, accuracies, marker="o", label="Accuracy")
plt.plot(train_sizes, f1_scores, marker="s", label="Macro F1")

plt.xlabel("Training Data Size (%)")
plt.ylabel("Score")
plt.title("SVM Baseline – Learning Curve")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
