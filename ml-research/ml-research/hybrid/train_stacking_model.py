# ==========================================================
# CLEAN OOF STACKING (SVM OOF + Frozen BERT)
# ==========================================================

import os
import sys
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ----------------------------------------------------------
# PATH SETUP
# ----------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from pipeline.analyze_clause import bert_predict

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "train_full.csv")
MODEL_OUTPUT = os.path.join(PROJECT_ROOT, "models", "stacked_meta_model.pkl")

N_SPLITS = 5
RANDOM_STATE = 42

print("📥 Loading training data...")
df = pd.read_csv(DATA_PATH)

X = df["clause_text"].values
y = df["label"].values

num_classes = len(set(y))

# ----------------------------------------------------------
# OOF SETUP
# ----------------------------------------------------------
skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)

oof_features = np.zeros((len(X), num_classes * 2))

print("🔁 Generating OOF features (SVM retrained per fold)...")

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):

    print(f"\n🚀 Fold {fold+1}/{N_SPLITS}")

    X_train_fold = X[train_idx]
    y_train_fold = y[train_idx]

    X_val_fold = X[val_idx]

    # --------------------------
    # Train SVM on fold
    # --------------------------
    vectorizer = TfidfVectorizer(
        max_features=60000,
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True,
        min_df=2
    )

    X_train_vec = vectorizer.fit_transform(X_train_fold)
    X_val_vec = vectorizer.transform(X_val_fold)

    base_svm = LinearSVC(
        class_weight="balanced",
        random_state=RANDOM_STATE,
        max_iter=5000
    )

    calibrated_svm = CalibratedClassifierCV(
        base_svm,
        method="sigmoid",
        cv=3
    )

    calibrated_svm.fit(X_train_vec, y_train_fold)

    svm_val_probs = calibrated_svm.predict_proba(X_val_vec)

    # --------------------------
    # BERT predictions (frozen)
    # --------------------------
    for i, idx in enumerate(val_idx):

        clause = X[idx]

        _, bert_probs = bert_predict(clause)

        combined = np.concatenate([bert_probs, svm_val_probs[i]])

        oof_features[idx] = combined

print("\nOOF feature matrix shape:", oof_features.shape)

# ----------------------------------------------------------
# TRAIN META MODEL
# ----------------------------------------------------------
print("\n🧠 Training meta-classifier on OOF features...")

meta_model = LogisticRegression(
    max_iter=3000,
    multi_class="multinomial",
    solver="lbfgs",
    n_jobs=-1
)

meta_model.fit(oof_features, y)

# Save
joblib.dump(meta_model, MODEL_OUTPUT)

print(f"\n💾 OOF stacked model saved → {MODEL_OUTPUT}")

# ----------------------------------------------------------
# OOF Training Performance
# ----------------------------------------------------------
pred_train = meta_model.predict(oof_features)

print("\n📊 OOF Training Performance:")
print("Accuracy :", round(accuracy_score(y, pred_train), 4))
print("Precision:", round(precision_score(y, pred_train, average="macro", zero_division=0), 4))
print("Recall   :", round(recall_score(y, pred_train, average="macro", zero_division=0), 4))
print("F1       :", round(f1_score(y, pred_train, average="macro", zero_division=0), 4))

print("\n✅ CLEAN OOF STACKING COMPLETE")