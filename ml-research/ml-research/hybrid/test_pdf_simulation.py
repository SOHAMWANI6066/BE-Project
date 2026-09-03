from hybrid.real_model_runner import bert_predict, svm_predict
from hybrid.hybrid_predictor import hybrid_predict

document = """
This Agreement shall be governed by the laws of India.
The agreement may be terminated by either party with thirty days notice.
The parties shall not disclose confidential information.
"""

clauses = [
    c.strip()
    for c in document.split(".")
    if len(c.strip()) > 10
]

print(f"Total clauses extracted: {len(clauses)}\n")

for i, clause in enumerate(clauses, 1):
    bert_label, bert_probs = bert_predict(clause)
    svm_label = svm_predict(clause)

    result = hybrid_predict(
        clause=clause,
        bert_label=bert_label,
        bert_probabilities=bert_probs,
        svm_label=svm_label
    )

    print(f"--- Clause {i} ---")
    print(clause)
    print("Final label:", result["final_label"])
    print("Used model:", result["used_model"])
    print()