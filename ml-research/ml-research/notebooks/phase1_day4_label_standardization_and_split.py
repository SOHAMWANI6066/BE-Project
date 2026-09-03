"""
PHASE 1 – DAY 4
Label Standardization + 80/20 Split + Learning Curve Datasets

This script:
1. Converts CUAD to single-label classification
2. Creates final_dataset.csv
3. Performs 80/20 train-test split
4. Generates training subsets for learning-curve charts
"""

import pandas as pd
import os
from sklearn.model_selection import train_test_split

# -----------------------------
# PATH CONFIG
# -----------------------------

BASE_DIR = "ml-research/data/processed"

CUAD_CLEAN_PATH = os.path.join(BASE_DIR, "cuad_clean.csv")

FINAL_DATASET_PATH = os.path.join(BASE_DIR, "final_dataset.csv")
TRAIN_FULL_PATH = os.path.join(BASE_DIR, "train_full.csv")
TEST_PATH = os.path.join(BASE_DIR, "test.csv")

# Training subset paths
TRAIN_SPLITS = {
    40: "train_40.csv",
    50: "train_50.csv",
    60: "train_60.csv",
    70: "train_70.csv",
    80: "train_80.csv",
    90: "train_90.csv",
    100: "train_100.csv",
}

# -----------------------------
# STEP 1: LOAD CLEAN CUAD
# -----------------------------

print("\n🔹 Loading cleaned CUAD dataset...")
df = pd.read_csv(CUAD_CLEAN_PATH)

print("Columns:", list(df.columns))
print("Original shape:", df.shape)

# -----------------------------
# STEP 2: SINGLE-LABEL STANDARDIZATION
# -----------------------------

print("\n🔹 Standardizing labels (single-label classification)...")

# Keep only positive clauses
df = df[df["answer"].str.lower() == "yes"]

# Keep only required columns
df = df[["clause_text", "label"]]

# Remove duplicates
df = df.drop_duplicates()

print("After label filtering:", df.shape)

# Save final dataset
df.to_csv(FINAL_DATASET_PATH, index=False)
print(f"📁 Saved final dataset: {FINAL_DATASET_PATH}")

# -----------------------------
# STEP 3: 80/20 TRAIN-TEST SPLIT
# -----------------------------

print("\n🔹 Creating 80/20 train-test split...")

train_full, test = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)

train_full.to_csv(TRAIN_FULL_PATH, index=False)
test.to_csv(TEST_PATH, index=False)

print("Train size (80%):", train_full.shape)
print("Test size (20%):", test.shape)

# -----------------------------
# STEP 4: CREATE LEARNING CURVE TRAINING SETS (STRATIFIED)
# -----------------------------

print("\n🔹 Creating training subsets for learning-curve charts (stratified)...")

for percent, filename in TRAIN_SPLITS.items():
    frac = percent / 100.0
    subsets = []

    for label, group in train_full.groupby("label"):
        group_subset = group.sample(
            frac=frac,
            random_state=42
        )
        subsets.append(group_subset)

    subset = pd.concat(subsets).sample(frac=1, random_state=42)  # shuffle

    subset_path = os.path.join(BASE_DIR, filename)
    subset.to_csv(subset_path, index=False)

    print(f"📁 Saved {filename} ({percent}% of training data): {subset.shape}")


# -----------------------------
# DONE
# -----------------------------

print("\n🎉 PHASE 1 – DAY 4 COMPLETED SUCCESSFULLY")
print("Datasets are now ready for model training and chart generation.")
