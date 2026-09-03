"""
Threshold configuration for Hybrid Model
These values are FIXED a priori and must not be tuned during evaluation.
"""

# --------------------------------------------------
# Class-wise confidence thresholds for DistilBERT
# --------------------------------------------------
CONFIDENCE_THRESHOLDS = {
    "Governing Law": 0.60,
    "Termination": 0.75,
    "Liability": 0.80,
    "Confidentiality": 0.70,
    "Default": 0.70
}

# --------------------------------------------------
# Global margin threshold (top1 - top2 probability)
# Used for normal-length clauses
# --------------------------------------------------
MARGIN_THRESHOLD = 0.15

# --------------------------------------------------
# Clause length cutoff (word count)
# Clauses <= this are considered SHORT and high-risk
# --------------------------------------------------
SHORT_CLAUSE_WORDS = 20

# --------------------------------------------------
# High-certainty thresholds for SHORT clauses
# Short clauses require stricter confidence & clarity
# --------------------------------------------------
HIGH_CONF_THRESHOLD = 0.90
HIGH_MARGIN_THRESHOLD = 0.30
