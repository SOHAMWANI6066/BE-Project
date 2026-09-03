import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report

# ---------------- PATH ----------------
RESULTS_PATH = "hybrid/results/hybrid_batch_results.csv"

print("📥 Loading hybrid batch results...")
df = pd.read_csv(RESULTS_PATH)

# ---------------- BASIC CHECKS ----------------
required_cols = [
    "true_label",
    "bert_label",
    "svm_label",
    "hybrid_label",
    "used_model",
    "short_clause"
]

for col in required_cols:
    assert col in df.columns, f"Missing column: {col}"

# ---------------- OVERALL METRICS ----------------
print("\n📊 OVERALL PERFORMANCE\n")

models = {
    "SVM": df["svm_label"],
    "DistilBERT": df["bert_label"],
    "Hybrid": df["hybrid_label"]
}

for name, preds in models.items():
    acc = accuracy_score(df["true_label"], preds)
    f1 = f1_score(df["true_label"], preds, average="macro")

    print(f"{name}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Macro F1 : {f1:.4f}\n")

# ---------------- SHORT CLAUSE ANALYSIS ----------------
print("\n📉 SHORT CLAUSE ANALYSIS (short_clause == True)\n")

short_df = df[df["short_clause"] == True]

for name, preds in {
    "SVM": short_df["svm_label"],
    "DistilBERT": short_df["bert_label"],
    "Hybrid": short_df["hybrid_label"]
}.items():
    acc = accuracy_score(short_df["true_label"], preds)
    f1 = f1_score(short_df["true_label"], preds, average="macro")

    print(f"{name}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Macro F1 : {f1:.4f}\n")

# ---------------- DECISION DISTRIBUTION ----------------
print("\n⚖️ HYBRID DECISION DISTRIBUTION\n")
print(df["used_model"].value_counts(normalize=True) * 100)

# ---------------- ERROR BY DECISION PATH ----------------
print("\n❌ ERROR RATE BY DECISION PATH\n")

for path in df["used_model"].unique():
    subset = df[df["used_model"] == path]
    error_rate = (subset["hybrid_label"] != subset["true_label"]).mean()

    print(f"{path}")
    print(f"  Samples    : {len(subset)}")
    print(f"  Error rate : {error_rate:.4f}\n")
