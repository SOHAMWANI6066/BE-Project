import pandas as pd

# ----------------------------------------
# PATHS
# ----------------------------------------
INPUT_CSV = "hybrid/results/active_learning_candidates.csv"
OUTPUT_CSV = "hybrid/results/pseudo_labeled_active_learning.csv"

# ----------------------------------------
# CONFIDENCE GATES (VERY STRICT)
# ----------------------------------------
BERT_STRONG_CONF = 0.85
BERT_STRONG_MARGIN = 0.30
AGREEMENT_CONF = 0.80

print("📥 Loading active learning candidates...")
df = pd.read_csv(INPUT_CSV)

print(f"Total candidates: {len(df)}")

# ----------------------------------------
# RULE A: Extremely confident DistilBERT
# ----------------------------------------
rule_a = (
    (df["used_model"] == "DistilBERT") &
    (df["bert_confidence"] >= BERT_STRONG_CONF) &
    (df["bert_margin"] >= BERT_STRONG_MARGIN)
)

# ----------------------------------------
# RULE B: Strong agreement
# ----------------------------------------
rule_b = (
    (df["used_model"] == "Agreement") &
    (df["bert_confidence"] >= AGREEMENT_CONF) &
    (df["bert_margin"] >= 0.25)
)

pseudo_df = df[rule_a | rule_b].copy()

print(f"Auto-correctable clauses selected: {len(pseudo_df)}")

# ----------------------------------------
# BUILD PSEUDO-LABELED DATASET
# ----------------------------------------
pseudo_df = pseudo_df[[
    "clause_text",
    "hybrid_label",
    "bert_confidence",
    "bert_margin",
    "used_model"
]]

pseudo_df = pseudo_df.rename(
    columns={"hybrid_label": "pseudo_label"}
)

pseudo_df["source"] = "hybrid_self_training"

# ----------------------------------------
# SAVE
# ----------------------------------------
pseudo_df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Pseudo-labeled dataset saved to: {OUTPUT_CSV}")
