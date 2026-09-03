import os
import pandas as pd
import torch
import joblib
import numpy as np
from tqdm import tqdm

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

from hybrid.hybrid_predictor import hybrid_predict


# ---------------- PATHS ----------------
TEST_DATA_PATH = "data/processed/test.csv"
SVM_MODEL_PATH = "models/svm_final.pkl"
BERT_MODEL_PATH = "models/distilbert_final"
OUTPUT_CSV_PATH = "hybrid/results/hybrid_batch_results.csv"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ---------------- LOAD TEST DATA ----------------
print("📥 Loading test dataset...")
df = pd.read_csv(TEST_DATA_PATH)

assert "clause_text" in df.columns, "Missing clause_text column"
assert "label" in df.columns, "Missing ground truth label column"


# ---------------- LOAD SVM ----------------
print("📦 Loading SVM...")
svm_bundle = joblib.load(SVM_MODEL_PATH)
svm_vectorizer = svm_bundle["vectorizer"]
svm_model = svm_bundle["model"]


# ---------------- LOAD DISTILBERT ----------------
print("📦 Loading DistilBERT...")
tokenizer = DistilBertTokenizerFast.from_pretrained(BERT_MODEL_PATH)
bert_model = DistilBertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
bert_model.to(DEVICE)
bert_model.eval()


# ---------------- INFERENCE HELPERS ----------------
def bert_predict(clause):
    inputs = tokenizer(
        clause,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = bert_model(**inputs)

    logits = outputs.logits.squeeze().cpu().numpy()
    probs = torch.softmax(torch.tensor(logits), dim=0).numpy()

    pred_id = int(np.argmax(probs))
    label = bert_model.config.id2label[pred_id]

    return label, probs.tolist()


def svm_predict(clause):
    vec = svm_vectorizer.transform([clause])
    return svm_model.predict(vec)[0]


# ---------------- BATCH EVALUATION ----------------
results = []

print("🚀 Running batch hybrid evaluation...")

for idx, row in tqdm(df.iterrows(), total=len(df)):
    clause = row["clause_text"]
    true_label = row["label"]

    bert_label, bert_probs = bert_predict(clause)
    svm_label = svm_predict(clause)

    hybrid_result = hybrid_predict(
        clause=clause,
        bert_label=bert_label,
        bert_probabilities=bert_probs,
        svm_label=svm_label
    )

    results.append({
        "clause_id": idx,
        "clause_text": clause,
        "true_label": true_label,

        "bert_label": bert_label,
        "svm_label": svm_label,

        "hybrid_label": hybrid_result["final_label"],
        "used_model": hybrid_result["used_model"],

        "bert_confidence": hybrid_result["bert_confidence"],
        "bert_margin": hybrid_result["bert_margin"],
        "clause_length": hybrid_result["clause_length"],
        "short_clause": hybrid_result["short_clause"]
    })


# ---------------- SAVE RESULTS ----------------
os.makedirs("hybrid/results", exist_ok=True)
out_df = pd.DataFrame(results)
out_df.to_csv(OUTPUT_CSV_PATH, index=False)

print(f"✅ Hybrid batch results saved to: {OUTPUT_CSV_PATH}")
