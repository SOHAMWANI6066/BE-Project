"""
PHASE 1 – DAY 3
Dataset Cleaning & Normalization Script

This script:
- Loads RAW datasets (CUAD + Kaggle datasets)
- Cleans and normalizes clause text
- Removes noise and duplicates
- Saves CLEANED datasets for modeling

IMPORTANT:
- Raw data is NOT modified
- No label mapping is done here
"""

import pandas as pd
import re
import os

# -----------------------------
# CONFIGURATION
# -----------------------------

# Base paths
BASE_DIR = "ml-research/data"
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# Input file paths (CHANGE FILENAMES ONLY if different)
CUAD_PATH = os.path.join(RAW_DIR, "cuad", "master_clauses.csv")
KAGGLE_GENERAL_PATH = os.path.join(RAW_DIR, "kaggle_general", "legal_docs.csv")
KAGGLE_INDIAN_PATH = os.path.join(RAW_DIR, "kaggle_indian", "legal_contract_clauses.csv")

# Output file paths
CUAD_OUT = os.path.join(PROCESSED_DIR, "cuad_clean.csv")
KAGGLE_GENERAL_OUT = os.path.join(PROCESSED_DIR, "kaggle_general_clean.csv")
KAGGLE_INDIAN_OUT = os.path.join(PROCESSED_DIR, "kaggle_indian_clean.csv")

# Create processed directory if not exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# -----------------------------
# CLEANING FUNCTION
# -----------------------------

def clean_clause_text(text):
    """
    Cleans legal clause text without destroying legal meaning.
    """
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    text = text.strip()

    return text


# -----------------------------
# STEP 1: FLATTEN + CLEAN CUAD DATASET
# -----------------------------

print("\n🔹 Flattening and cleaning CUAD dataset...")

cuad_df = pd.read_csv(CUAD_PATH)

# Identify clause columns (those NOT ending with '-Answer')
clause_columns = [col for col in cuad_df.columns if not col.endswith("-Answer")]

records = []

for _, row in cuad_df.iterrows():
    for clause_col in clause_columns:
        answer_col = clause_col + "-Answer"

        if answer_col not in cuad_df.columns:
            continue

        clause_text = row[clause_col]
        label = row[answer_col]

        # Skip empty clauses
        if pd.isna(clause_text) or str(clause_text).strip() == "":
            continue

        cleaned_text = clean_clause_text(clause_text)

        # Skip very short clauses
        if len(cleaned_text.split()) < 10:
            continue

        records.append({
            "clause_text": cleaned_text,
            "label": clause_col,
            "answer": label
        })

cuad_flat_df = pd.DataFrame(records)

# Remove duplicates
cuad_flat_df = cuad_flat_df.drop_duplicates(subset=["clause_text", "label"])

print(f"✅ CUAD flattened shape: {cuad_flat_df.shape}")

# Save cleaned & flattened CUAD
cuad_flat_df.to_csv(CUAD_OUT, index=False)
print(f"📁 Saved: {CUAD_OUT}")



# -----------------------------
# STEP 2: CLEAN KAGGLE GENERAL DATASET
# -----------------------------

print("\n🔹 Cleaning Kaggle General Contracts dataset...")

kaggle_general_df = pd.read_csv(KAGGLE_GENERAL_PATH)

print("Kaggle General columns:", list(kaggle_general_df.columns))

# ASSUMED column names (change ONLY if needed)
# Correct Kaggle General column names
GEN_TEXT_COL = "clause_text"
GEN_LABEL_COL = "clause_type"


kaggle_general_df[GEN_TEXT_COL] = kaggle_general_df[GEN_TEXT_COL].apply(clean_clause_text)

# Remove empty clauses
kaggle_general_df = kaggle_general_df[kaggle_general_df[GEN_TEXT_COL] != ""]

# Remove very short clauses
kaggle_general_df = kaggle_general_df[
    kaggle_general_df[GEN_TEXT_COL].str.split().str.len() >= 10
]

# Remove rows without labels
kaggle_general_df = kaggle_general_df.dropna(subset=[GEN_LABEL_COL])

# Remove duplicates
kaggle_general_df = kaggle_general_df.drop_duplicates(subset=[GEN_TEXT_COL])

print(f"✅ Kaggle General cleaned shape: {kaggle_general_df.shape}")

# Save cleaned Kaggle General
kaggle_general_df.to_csv(KAGGLE_GENERAL_OUT, index=False)
print(f"📁 Saved: {KAGGLE_GENERAL_OUT}")


# -----------------------------
# STEP 3: CLEAN KAGGLE INDIAN DATASET
# -----------------------------

print("\n🔹 Cleaning Kaggle Indian Contracts dataset...")

kaggle_indian_df = pd.read_csv(KAGGLE_INDIAN_PATH)

print("Kaggle Indian columns:", list(kaggle_indian_df.columns))

# ASSUMED column names (change ONLY if needed)
# Correct Kaggle Indian column names
IND_TEXT_COL = "clause_text"
IND_LABEL_COL = "clause_type"


kaggle_indian_df[IND_TEXT_COL] = kaggle_indian_df[IND_TEXT_COL].apply(clean_clause_text)

# Remove empty clauses
kaggle_indian_df = kaggle_indian_df[kaggle_indian_df[IND_TEXT_COL] != ""]

# Remove very short clauses
kaggle_indian_df = kaggle_indian_df[
    kaggle_indian_df[IND_TEXT_COL].str.split().str.len() >= 10
]

# Remove rows without labels
kaggle_indian_df = kaggle_indian_df.dropna(subset=[IND_LABEL_COL])

# Remove duplicates
kaggle_indian_df = kaggle_indian_df.drop_duplicates(subset=[IND_TEXT_COL])

print(f"✅ Kaggle Indian cleaned shape: {kaggle_indian_df.shape}")

# Save cleaned Kaggle Indian
kaggle_indian_df.to_csv(KAGGLE_INDIAN_OUT, index=False)
print(f"📁 Saved: {KAGGLE_INDIAN_OUT}")


# -----------------------------
# FINAL CONFIRMATION
# -----------------------------

print("\n🎉 PHASE 1 – DAY 3 COMPLETED SUCCESSFULLY")
print("Cleaned datasets created:")
print(" - cuad_clean.csv")
print(" - kaggle_general_clean.csv")
print(" - kaggle_indian_clean.csv")
