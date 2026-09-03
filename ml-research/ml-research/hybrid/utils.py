"""
Utility functions for Hybrid Model
These functions extract signals used by the decision controller.
"""

from typing import List
from .thresholds import CONFIDENCE_THRESHOLDS, MARGIN_THRESHOLD, SHORT_CLAUSE_WORDS


def get_clause_length(clause: str) -> int:
    """
    Returns number of words in a clause.
    """
    if not clause or not isinstance(clause, str):
        return 0
    return len(clause.strip().split())


def is_short_clause(clause: str) -> bool:
    """
    Determines whether a clause is considered short.
    """
    return get_clause_length(clause) <= SHORT_CLAUSE_WORDS


def get_bert_confidence(probabilities: List[float]) -> float:
    """
    Returns the maximum softmax probability.
    """
    if not probabilities:
        return 0.0
    return float(max(probabilities))


def get_bert_margin(probabilities: List[float]) -> float:
    """
    Returns difference between top-1 and top-2 probabilities.
    """
    if not probabilities or len(probabilities) < 2:
        return 0.0

    sorted_probs = sorted(probabilities, reverse=True)
    return float(sorted_probs[0] - sorted_probs[1])


def get_confidence_threshold(label: str) -> float:
    """
    Fetches class-wise confidence threshold.
    Falls back to default if class not found.
    """
    return CONFIDENCE_THRESHOLDS.get(label, CONFIDENCE_THRESHOLDS["Default"])
