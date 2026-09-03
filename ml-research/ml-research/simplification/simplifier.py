"""
Clause Simplification Module (Production Stable)

Order:
1. Very short → already simple
2. Rule-based (primary)
3. Safe fallback
"""

import logging
import re
from difflib import SequenceMatcher

from .rules import rule_based_simplify


logging.getLogger("transformers").setLevel(logging.ERROR)


# --------------------------------------------------
# UTILITIES
# --------------------------------------------------

def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def is_valid_output(original: str, candidate: str) -> bool:
    if not candidate:
        return False

    if len(candidate.split()) > len(original.split()):
        return False

    if similarity(original, candidate) > 0.93:
        return False

    if len(candidate.split()) < 4:
        return False

    return True


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def simplify_clause(clause_text: str, clause_type: str) -> dict:

    clause_text = clean_text(clause_text)
    words = clause_text.split()

    # 1️⃣ Very short → already simple
    if len(words) <= 4:
        return {
            "simplified_text": clause_text,
            "method": "already_simple"
        }

    # 2️⃣ Rule-based
    rule_result = rule_based_simplify(clause_text, clause_type)

    if rule_result:
        rule_result = clean_text(rule_result)
        if is_valid_output(clause_text, rule_result):
            return {
                "simplified_text": rule_result,
                "method": "rule_based"
            }

    # 3️⃣ Safe fallback
    return {
        "simplified_text": clause_text,
        "method": "fallback"
    }