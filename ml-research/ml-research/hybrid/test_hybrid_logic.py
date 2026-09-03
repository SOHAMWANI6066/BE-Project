from .hybrid_predictor import hybrid_predict
# ---------------- TEST CASES ----------------

def run_test(test_name, clause, bert_label, bert_probs, svm_label):
    print(f"\n=== {test_name} ===")
    result = hybrid_predict(
        clause=clause,
        bert_label=bert_label,
        bert_probabilities=bert_probs,
        svm_label=svm_label
    )
    for k, v in result.items():
        print(f"{k}: {v}")


# Case 1: Strong DistilBERT (should trust BERT)
run_test(
    test_name="CASE 1: Strong BERT",
    clause="The agreement may be terminated by either party with thirty days prior written notice upon occurrence of a material breach of contractual obligations.",
    bert_label="Termination",
    bert_probs=[0.82, 0.08, 0.05, 0.05],
    svm_label="Termination"
)

# Case 2: Low confidence, agreement (should accept agreement)
run_test(
    test_name="CASE 2: Agreement, low confidence",
    clause="This agreement terminates.",
    bert_label="Termination",
    bert_probs=[0.55, 0.25, 0.10, 0.10],
    svm_label="Termination"
)

# Case 3: Confident but confused (low margin → fallback)
run_test(
    test_name="CASE 3: Low margin confusion",
    clause="The agreement may be terminated.",
    bert_label="Termination",
    bert_probs=[0.45, 0.43, 0.07, 0.05],
    svm_label="Liability"
)

# Case 4: Short clause, disagreement (should fallback to SVM)
run_test(
    test_name="CASE 4: Short clause disagreement",
    clause="Agreement terminates.",
    bert_label="Termination",
    bert_probs=[0.78, 0.12, 0.05, 0.05],
    svm_label="Confidentiality"
)

# Case 5: Long clause, low confidence (should fallback)
run_test(
    test_name="CASE 5: Long clause, low confidence",
    clause="The agreement may be terminated by either party upon breach of material obligations under applicable law.",
    bert_label="Termination",
    bert_probs=[0.60, 0.20, 0.10, 0.10],
    svm_label="Termination"
)
