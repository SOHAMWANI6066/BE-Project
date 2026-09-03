"""
Intelligent Label Correction Layer (ILCL)
----------------------------------------
Applies semantic corrections to hybrid predictions
when model confusion is structurally obvious.

Designed for CUAD commercial contracts.
"""

import re


# ============================================================
# TEXT SIGNAL DETECTORS
# ============================================================

def contains_usage_limit(text: str) -> bool:
    return bool(
        re.search(
            r'(authorized users?|user seats?|volume restriction|limit(ed)? to|maximum of \d+)',
            text,
            re.IGNORECASE
        )
    )


def contains_audit_signal(text: str) -> bool:
    return bool(
        re.search(
            r'(audit|inspect|review records?|verify compliance)',
            text,
            re.IGNORECASE
        )
    )


def contains_confidential_signal(text: str) -> bool:
    return bool(
        re.search(
            r'(confidential|confidentiality|trade secret|proprietary information|non-disclosure)',
            text,
            re.IGNORECASE
        )
    )


def contains_ip_signal(text: str) -> bool:
    return bool(
        re.search(
            r'(intellectual property|ip ownership|shall remain owned|ownership of)',
            text,
            re.IGNORECASE
        )
    )


def contains_non_solicit_signal(text: str) -> bool:
    return bool(
        re.search(
            r'(solicit|hire employees?|no-solicit)',
            text,
            re.IGNORECASE
        )
    )


def contains_non_compete_signal(text: str) -> bool:
    return bool(
        re.search(
            r'(compete|competing products?|market competing)',
            text,
            re.IGNORECASE
        )
    )


def contains_uncapped_liability_signal(text: str) -> bool:
    return bool(
        re.search(
            r'(shall not apply|unlimited liability|fraud|willful misconduct|uncapped)',
            text,
            re.IGNORECASE
        )
    )


# ============================================================
# CORRECTION ENGINE
# ============================================================

def apply_label_correction(
    clause: str,
    predicted_label: str
) -> str:

    text = clause.strip()
    label = predicted_label

    # --------------------------------------------------
    # 1️⃣ Volume Restriction vs Audit Rights confusion
    # --------------------------------------------------
    if label == "Audit Rights":
        if contains_usage_limit(text) and not contains_audit_signal(text):
            return "Volume Restriction"

    # --------------------------------------------------
    # 2️⃣ Audit misclassified as Volume Restriction
    # --------------------------------------------------
    if label == "Volume Restriction":
        if contains_audit_signal(text):
            return "Audit Rights"

    # --------------------------------------------------
    # 3️⃣ Confidentiality confusion
    # CUAD does not have explicit Confidentiality label.
    # Closest semantic class often confused with liability.
    # We DO NOT override unless clearly wrong.
    # --------------------------------------------------
    if contains_confidential_signal(text):
        # If wrongly classified as liability
        if label in ["Uncapped Liability", "Cap On Liability"]:
            return "Non-Disparagement"

    # --------------------------------------------------
    # 4️⃣ IP Ownership vs Assignment confusion
    # --------------------------------------------------
    if label == "Anti-Assignment":
        if contains_ip_signal(text):
            return "Ip Ownership Assignment"

    # --------------------------------------------------
    # 5️⃣ Non-Solicit vs Non-Compete confusion
    # --------------------------------------------------
    if label == "Non-Compete":
        if contains_non_solicit_signal(text):
            return "No-Solicit Of Employees"

    if label == "No-Solicit Of Employees":
        if contains_non_compete_signal(text):
            return "Non-Compete"
        # --------------------------------------------------
    # 6️⃣ Uncapped Liability semantic reinforcement
    # --------------------------------------------------
    if contains_uncapped_liability_signal(text):
        return "Uncapped Liability"

    # --------------------------------------------------
    # Default → no correction
    # --------------------------------------------------
    return label