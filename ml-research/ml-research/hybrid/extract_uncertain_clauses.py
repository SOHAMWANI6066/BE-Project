import pandas as pd

# --------------------------------------------------
# PATHS
# --------------------------------------------------
INPUT_CSV = "hybrid/results/hybrid_batch_results.csv"
OUTPUT_CSV = "hybrid/results/active_learning_candidates.csv"

# Safety margins
CONF_EPS = 0.05
MARGIN_EPS = 0.05
BASE_MARGIN_THRESHOLD = 0.15

print("📥 Loading hybrid batch results...")
df = pd.read_csv(INPUT_CSV)

# --------------------------------------------------
# BASIC SANITY CHECKS
# --------------------------------------------------
required_cols = [
    "clause_text",
    "true_label",
    "hybrid_label",
    "used_model",
    "bert_confidence",
    "bert_margin",
    "clause_length"
]

for col in required_cols:
    assert col in df.columns, f"Missing column: {col}"

print(f"Total clauses: {len(df)}")

# --------------------------------------------------
# UNCERTAINTY RULES
# --------------------------------------------------

# U1: Hybrid did not trust DistilBERT
u1 = df["used_model"].isin(["SVM", "Agreement"])

# U2: Hybrid prediction is wrong
u2 = df["hybrid_label"] != df["true_label"]

# U3: Borderline DistilBERT cases
u3 = (
    (df["used_model"] == "DistilBERT") &
    (
        (df["bert_confidence"] < 0.75 + CONF_EPS) |
        (df["bert_margin"] < BASE_MARGIN_THRESHOLD + MARGIN_EPS)
    )
)

# Combine uncertainty
uncertain_mask = u1 | u2 | u3
uncertain_df = df[uncertain_mask].copy()

print(f"Uncertain clauses before filtering: {len(uncertain_df)}")

# --------------------------------------------------
# HARD FILTER: remove ultra-short clauses
# --------------------------------------------------
uncertain_df = uncertain_df[uncertain_df["clause_length"] >= 5]

print(f"Uncertain clauses after length filter: {len(uncertain_df)}")

# --------------------------------------------------
# PRIORITY SCORING (VERY IMPORTANT)
# --------------------------------------------------
def compute_priority(row):
    score = 0.0

    # Highest risk: wrong prediction
    if row["hybrid_label"] != row["true_label"]:
        score += 2.0

    # SVM fallback is riskier than agreement
    if row["used_model"] == "SVM":
        score += 1.0
    elif row["used_model"] == "Agreement":
        score += 0.5

  # Borderline confidence (global, conservative cutoff)
    if row["bert_confidence"] < 0.75 + CONF_EPS:
        score += 0.5

    if row["bert_margin"] < BASE_MARGIN_THRESHOLD + MARGIN_EPS:
        score += 0.5

    return score


uncertain_df["priority_score"] = uncertain_df.apply(compute_priority, axis=1)

# --------------------------------------------------
# SORT BY PRIORITY
# --------------------------------------------------
uncertain_df = uncertain_df.sort_values(
    by="priority_score",
    ascending=False
)

# --------------------------------------------------
# SELECT COLUMNS FOR HUMAN LABELING
# --------------------------------------------------
final_cols = [
    "clause_text",
    "true_label",
    "hybrid_label",
    "used_model",
    "bert_confidence",
    "bert_margin",
    "priority_score"
]

final_df = uncertain_df[final_cols]

# Add empty column for manual correction
final_df["human_corrected_label"] = ""

# --------------------------------------------------
# SAVE
# --------------------------------------------------
final_df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Active learning candidates saved to: {OUTPUT_CSV}")
print(f"📌 Total candidates: {len(final_df)}")
