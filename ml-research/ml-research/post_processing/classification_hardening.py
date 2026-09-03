"""
Advanced Post-Classification Hardening Layer

Purpose:
Stabilize ML predictions using weighted legal pattern detection.
Designed for CUAD-style contracts.

This does NOT blindly override ML.
It corrects only when strong legal evidence exists.
"""

import re


# ---------------------------------------------------------
# 🔎 LEGAL PATTERN DEFINITIONS (Weighted)
# ---------------------------------------------------------

PATTERN_RULES = {
    "Governing Law": [
        r"governed by the laws of",
        r"shall be governed by",
        r"laws of the state of",
        r"laws of india",
        r"laws of new york",
    ],

    "Indemnification": [
        r"indemnify",
        r"hold harmless",
        r"defend and indemnify",
        r"claims arising from",
    ],

    "Cap On Liability": [
        r"limitation of liability",
        r"total liability shall not exceed",
        r"liability shall not exceed",
        r"cap on liability",
    ],

    "Audit Rights": [
        r"right to audit",
        r"reserves the right to audit",
        r"audit .* records",
    ],

    "Non-Transferable License": [
        r"non-transferable license",
        r"non exclusive.*license",
        r"license granted.*non-transferable",
    ],

    "Termination For Convenience": [
        r"termination for convenience",
        r"may terminate this agreement",
        r"terminate upon .* notice",
        r"prior written notice",
    ],

    "Non-Compete": [
        r"non-compete",
        r"shall not compete",
        r"engage in competing business",
    ],

    "Confidentiality": [
        r"confidential information",
        r"shall not disclose",
        r"non-disclosure",
    ],

    "Exclusivity": [
        r"exclusive right",
        r"sole and exclusive",
        r"exclusivity period",
    ],
}


# ---------------------------------------------------------
# 🧠 SCORING ENGINE
# ---------------------------------------------------------

def harden_classification(clause_text: str, predicted_label: str) -> str:
    text = clause_text.lower()

    scores = {}

    for label, patterns in PATTERN_RULES.items():
        score = 0

        for pattern in patterns:
            if re.search(pattern, text):
                score += 1

        if score > 0:
            scores[label] = score

    # No strong signal → keep ML output
    if not scores:
        return predicted_label

    # Get highest scoring label
    best_label = max(scores, key=scores.get)
    best_score = scores[best_label]

    # Only override if signal is strong
    # (at least 2 keyword matches OR ML prediction completely unrelated)
    if best_score >= 2:
        return best_label

    # If ML prediction already matches pattern label → keep it
    if predicted_label == best_label:
        return predicted_label

    # Otherwise keep ML (avoid over-aggressive correction)
    return predicted_label