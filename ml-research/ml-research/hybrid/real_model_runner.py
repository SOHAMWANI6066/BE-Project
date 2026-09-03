import torch
import joblib
import numpy as np

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

from hybrid.hybrid_predictor import hybrid_predict


# --------------------------------------------------
# PATHS (relative to ml-research/)
# --------------------------------------------------
SVM_MODEL_PATH = "models/svm_final.pkl"
BERT_MODEL_PATH = "models/distilbert_self_trained"   # ✅ UPDATED

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# --------------------------------------------------
# LOAD SVM (MODEL + VECTORIZER)
# --------------------------------------------------
print("📦 Loading SVM model...")

svm_bundle = joblib.load(SVM_MODEL_PATH)

# Expecting: {"vectorizer": ..., "model": ...}
svm_vectorizer = svm_bundle["vectorizer"]
svm_model = svm_bundle["model"]


# --------------------------------------------------
# LOAD DISTILBERT (SELF-TRAINED)
# --------------------------------------------------
print("📦 Loading DistilBERT model & tokenizer...")

tokenizer = DistilBertTokenizerFast.from_pretrained(BERT_MODEL_PATH)
bert_model = DistilBertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)

bert_model.to(DEVICE)
bert_model.eval()


# --------------------------------------------------
# DISTILBERT INFERENCE
# --------------------------------------------------
def bert_predict(clause: str):
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


# --------------------------------------------------
# SVM INFERENCE
# --------------------------------------------------
def svm_predict(clause: str):
    features = svm_vectorizer.transform([clause])
    return svm_model.predict(features)[0]


# --------------------------------------------------
# REAL HYBRID RUN (ENTRY POINT)
# --------------------------------------------------
if __name__  == "__main__":

    test_clause = (
        "The agreement may be terminated by either party with thirty days prior "
        "written notice in the event of a material breach of contractual obligations."
    )

    print("\n📄 Clause:")
    print(test_clause)

    # DistilBERT prediction
    bert_label, bert_probs = bert_predict(test_clause)

    # SVM prediction
    svm_label = svm_predict(test_clause)

    # Hybrid decision
    result = hybrid_predict(
        clause=test_clause,
        bert_label=bert_label,
        bert_probabilities=bert_probs,
        svm_label=svm_label
    )

    print("\n🧠 DistilBERT Prediction:", bert_label)
    print("🧠 SVM Prediction:", svm_label)

    print("\n⚖️ Hybrid Decision:")
    for key, value in result.items():
        print(f"{key}: {value}")