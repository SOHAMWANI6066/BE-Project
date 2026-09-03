
# =====================================================
# RESEARCH-GRADE SVM TRAINING & EVALUATION
# - 80/20 frozen test split
# - Learning curve (40–100%)
# - Class balancing
# - Hyperparameter tuning (C search)
# - Probability calibration
# - Clean macro metrics
# - Final calibrated model saved
# =====================================================

import os
import json
import time
import joblib
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.preprocessing import label_binarize


# =====================================================
# ABSOLUTE PATH CONFIG (FIXED)
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
METRICS_DIR = os.path.join(BASE_DIR, "metrics")

TRAIN_FULL_FILE = "train_full.csv"
TEST_FILE = "test.csv"

TRAIN_SUBSETS = {
    40: "train_40.csv",
    50: "train_50.csv",
    60: "train_60.csv",
    70: "train_70.csv",
    80: "train_80.csv",
    90: "train_90.csv",
    100: "train_100.csv"
}

FINAL_MODEL_PATH = os.path.join(MODEL_DIR, "svm_final.pkl")
LEARNING_CURVE_JSON = os.path.join(METRICS_DIR, "svm_learning_curve.json")
FINAL_METRICS_JSON = os.path.join(METRICS_DIR, "svm_final_metrics.json")

RANDOM_STATE = 42

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)


# =====================================================
# LOAD TEST SET
# =====================================================

print("📥 Loading frozen test set...")
test_df = pd.read_csv(os.path.join(DATA_DIR, TEST_FILE))

X_test = test_df["clause_text"]
y_test = test_df["label"]

labels = sorted(y_test.unique())
y_test_bin = label_binarize(y_test, classes=labels)


# =====================================================
# TF-IDF VECTORIZER (Improved)
# =====================================================

print("🧠 Initializing TF-IDF...")

vectorizer = TfidfVectorizer(
    max_features=60000,
    ngram_range=(1, 2),
    stop_words="english",
    sublinear_tf=True,
    min_df=2
)

learning_curve_results = {}


# =====================================================
# LEARNING CURVE TRAINING
# =====================================================

for percent, file_name in TRAIN_SUBSETS.items():

    print(f"\n🚀 Training SVM with {percent}% of TRAIN data")

    train_df = pd.read_csv(os.path.join(DATA_DIR, file_name))

    X_train = train_df["clause_text"]
    y_train = train_df["label"]

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    base_svm = LinearSVC(
        class_weight="balanced",
        random_state=RANDOM_STATE,
        max_iter=5000
    )

    param_grid = {"C": [0.1, 0.5, 1.0, 2.0]}

    grid = GridSearchCV(
        base_svm,
        param_grid,
        scoring="f1_macro",
        cv=3,
        n_jobs=-1
    )

    start_time = time.time()
    grid.fit(X_train_vec, y_train)
    train_time = time.time() - start_time

    best_svm = grid.best_estimator_

    calibrated_model = CalibratedClassifierCV(
        best_svm,
        method="sigmoid",
        cv=3
    )

    calibrated_model.fit(X_train_vec, y_train)

    y_pred = calibrated_model.predict(X_test_vec)
    y_prob = calibrated_model.predict_proba(X_test_vec)

    roc_auc = roc_auc_score(
        y_test_bin,
        y_prob,
        average="macro",
        multi_class="ovr"
    )

    learning_curve_results[str(percent)] = {


"accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, average="macro", zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, average="macro", zero_division=0), 4),
        "f1_score": round(f1_score(y_test, y_pred, average="macro", zero_division=0), 4),
        "roc_auc": round(roc_auc, 4),
        "train_time_sec": round(train_time, 2)
    }

    print("   Best C:", grid.best_params_["C"])
    print("   Accuracy:", learning_curve_results[str(percent)]["accuracy"])
    print("   Macro F1:", learning_curve_results[str(percent)]["f1_score"])


with open(LEARNING_CURVE_JSON, "w") as f:
    json.dump(learning_curve_results, f, indent=4)

print(f"\n📊 Learning curve saved → {LEARNING_CURVE_JSON}")


# =====================================================
# FINAL MODEL TRAINING (100% TRAIN_FULL)
# =====================================================

print("\n🔥 Training FINAL SVM model on 100% TRAIN_FULL")

train_full_df = pd.read_csv(os.path.join(DATA_DIR, TRAIN_FULL_FILE))

X_train_full = train_full_df["clause_text"]
y_train_full = train_full_df["label"]

X_train_full_vec = vectorizer.fit_transform(X_train_full)
X_test_vec = vectorizer.transform(X_test)

base_svm = LinearSVC(
    class_weight="balanced",
    random_state=RANDOM_STATE,
    max_iter=5000
)

param_grid = {"C": [0.1, 0.5, 1.0, 2.0]}

grid = GridSearchCV(
    base_svm,
    param_grid,
    scoring="f1_macro",
    cv=3,
    n_jobs=-1
)

start_time = time.time()
grid.fit(X_train_full_vec, y_train_full)
final_train_time = time.time() - start_time

best_svm = grid.best_estimator_

calibrated_model = CalibratedClassifierCV(
    best_svm,
    method="sigmoid",
    cv=3
)

calibrated_model.fit(X_train_full_vec, y_train_full)

y_final_pred = calibrated_model.predict(X_test_vec)
y_final_prob = calibrated_model.predict_proba(X_test_vec)

final_metrics = {
    "accuracy": round(accuracy_score(y_test, y_final_pred), 4),
    "precision": round(precision_score(y_test, y_final_pred, average="macro", zero_division=0), 4),
    "recall": round(recall_score(y_test, y_final_pred, average="macro", zero_division=0), 4),
    "f1_score": round(f1_score(y_test, y_final_pred, average="macro", zero_division=0), 4),
    "roc_auc": round(
        roc_auc_score(
            y_test_bin,
            y_final_prob,
            average="macro",
            multi_class="ovr"
        ), 4
    ),
    "train_time_sec": round(final_train_time, 2)
}

joblib.dump(
    {"model": calibrated_model, "vectorizer": vectorizer},
    FINAL_MODEL_PATH
)

with open(FINAL_METRICS_JSON, "w") as f:
    json.dump(final_metrics, f, indent=4)

print(f"\n💾 Final model saved → {FINAL_MODEL_PATH}")
print(f"📊 Final metrics saved → {FINAL_METRICS_JSON}")
print("\n✅ OPTIMIZED SVM TRAINING COMPLETE")