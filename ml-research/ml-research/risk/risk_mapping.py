"""
Risk Mapping Module

This module assigns a legal risk level to a clause
based on its classified clause type.

IMPORTANT:
- This is NOT a machine learning model.
- Risk is derived using domain-driven rules.
- This ensures interpretability, stability, and legal safety.
"""

# --------------------------------------------------
# RISK LEVEL DEFINITIONS
# --------------------------------------------------
HIGH_RISK = "High"
MEDIUM_RISK = "Medium"
LOW_RISK = "Low"


# --------------------------------------------------
# CLAUSE TYPE → RISK LEVEL MAPPING
# --------------------------------------------------
RISK_BY_CLAUSE_TYPE = {

    # 🔴 HIGH RISK
    # Clauses that can cause financial loss, lawsuits,
    # or major contractual imbalance.
    "Liability": HIGH_RISK,
    "Uncapped Liability": HIGH_RISK,
    "Cap On Liability": HIGH_RISK,
    "Indemnification": HIGH_RISK,
    "Termination For Convenience": HIGH_RISK,
    "Non-Compete": HIGH_RISK,
    "Liquidated Damages": HIGH_RISK,
    "Warranty Duration": HIGH_RISK,

    # 🟠 MEDIUM RISK
    # Clauses that affect rights, obligations,
    # jurisdiction, or control but are usually standard.
    "Confidentiality": MEDIUM_RISK,
    "Governing Law": MEDIUM_RISK,
    "Audit Rights": MEDIUM_RISK,
    "Change Of Control": MEDIUM_RISK,
    "Insurance": MEDIUM_RISK,
    "Third Party Beneficiary": MEDIUM_RISK,
    "Assignment": MEDIUM_RISK,

    # 🟢 LOW RISK
    # Informational or procedural clauses.
    "Notice": LOW_RISK,
    "Definitions": LOW_RISK,
    "Interpretation": LOW_RISK,
    "General": LOW_RISK
}


# --------------------------------------------------
# DEFAULT RISK (SAFE FALLBACK)
# --------------------------------------------------
DEFAULT_RISK = MEDIUM_RISK


# --------------------------------------------------
# PUBLIC FUNCTION
# --------------------------------------------------
def get_clause_risk(clause_type: str) -> str:
    """
    Returns the risk level for a given clause type.

    Parameters:
    - clause_type (str): Classified clause type

    Returns:
    - str: Risk level (High / Medium / Low)
    """

    if not clause_type:
        return DEFAULT_RISK

    return RISK_BY_CLAUSE_TYPE.get(clause_type, DEFAULT_RISK)