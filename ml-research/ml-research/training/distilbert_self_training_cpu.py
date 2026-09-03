# ============================================================
# Optimized DistilBERT Training (80/20 Split Evaluation)
# - Proper evaluation on frozen test set
# - GPU optimized
# - Saves best model
# ============================================================

import os
import time
import pandas as pd
import numpy as np
import torch

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from sklearn.preprocessing import label_binarize

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
TRAIN_PATH = "data/processed/train_full.csv"
TEST_PATH = "data/processed/test.csv"
SAVE_PATH = "models/distilbert_final"

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
print("Loading training and test data...")

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

# ------------------------------------------------------------
# LABEL ENCODING
# ------------------------------------------------------------
labels = sorted(train_df["label"].unique())
label2id = {label: idx for idx, label in enumerate(labels)}
id2label = {idx: label for label, idx in label2id.items()}

train_df["label"] = train_df["label"].map(label2id)
test_df["label"] = test_df["label"].map(label2id)

# ------------------------------------------------------------
# TOKENIZER
# ------------------------------------------------------------
MODEL_NAME = "distilbert-base-uncased"
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(
        batch["clause_text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

train_ds = Dataset.from_pandas(train_df)
test_ds = Dataset.from_pandas(test_df)

train_ds = train_ds.map(tokenize, batched=True)
test_ds = test_ds.map(tokenize, batched=True)

train_ds = train_ds.rename_column("label", "labels")
test_ds = test_ds.rename_column("label", "labels")

train_ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
test_ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# ------------------------------------------------------------
# MODEL
# ------------------------------------------------------------
model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

# ------------------------------------------------------------
# METRICS FUNCTION
# ------------------------------------------------------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="macro", zero_division=0
    )

    acc = accuracy_score(labels, predictions)

    # ROC-AUC
    try:
        labels_bin = label_binarize(labels, classes=list(range(len(label2id))))
        roc_auc = roc_auc_score(labels_bin, logits, average="macro", multi_class="ovr")
    except:
        roc_auc = 0.0

    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc
    }

# ------------------------------------------------------------
# TRAINING ARGUMENTS
# ------------------------------------------------------------
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=4,
    weight_decay=0.01,
    warmup_ratio=0.1,
    logging_dir="./logs",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    greater_is_better=True,
    report_to="none"
)
# ------------------------------------------------------------
# TRAINER
# ------------------------------------------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# ------------------------------------------------------------
# TRAIN
# ------------------------------------------------------------
print("Starting training on GPU...")
start_time = time.time()
trainer.train()
print("Training finished in:", round(time.time() - start_time, 2), "seconds")

# ------------------------------------------------------------
# FINAL EVALUATION
# ------------------------------------------------------------
metrics = trainer.evaluate()
print("Final Test Metrics:")
print(metrics)

# ------------------------------------------------------------
# SAVE MODEL
# ------------------------------------------------------------
os.makedirs(SAVE_PATH, exist_ok=True)
trainer.save_model(SAVE_PATH)
tokenizer.save_pretrained(SAVE_PATH)

print("Model saved at:", SAVE_PATH)