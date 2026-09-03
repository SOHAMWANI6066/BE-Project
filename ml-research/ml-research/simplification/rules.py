"""
High-Level Rule-Based Legal Clause Simplification (CUAD Aligned)
----------------------------------------------------------------
Exact-label driven.
Value-preserving.
No cross-category contamination.
"""

import re


# ============================================================
# VALUE EXTRACTORS
# ============================================================

def extract_duration(text: str):
    match = re.search(
        r'(\d+\s*(?:day|days|month|months|year|years))',
        text,
        re.IGNORECASE
    )
    return match.group(1) if match else None


def extract_money_cap(text: str):
    match = re.search(
        r'(\$\s?\d+[,\d]*(?:\.\d{1,2})?)',
        text
    )
    return match.group(1) if match else None


def extract_jurisdiction(text: str):
    match = re.search(
        r'laws of ([A-Za-z\s]+)',
        text,
        re.IGNORECASE
    )
    return match.group(1).strip() if match else None


# ============================================================
# MAIN RULE ENGINE
# ============================================================

def rule_based_simplify(clause: str, clause_type: str):

    if not clause or not clause_type:
        return None

    label = clause_type.strip()
    text = clause.strip()

    # ========================================================
    # TERMINATION
    # ========================================================

    if label == "Termination For Convenience":
        duration = extract_duration(text)
        if duration:
            return f"Either party may terminate this agreement with {duration} notice."
        return "Either party may terminate this agreement under defined conditions."

    if label == "Post-Termination Services":
        return "Certain services must continue after the agreement ends."

    # ========================================================
    # GOVERNING LAW
    # ========================================================

    if label == "Governing Law":
        jurisdiction = extract_jurisdiction(text)
        if jurisdiction:
            return f"This agreement is governed by the laws of {jurisdiction}."
        return "This agreement specifies which jurisdiction's laws apply."

    # ========================================================
    # CONFIDENTIALITY & NON-DISCLOSURE
    # ========================================================

    if label == "Non-Disparagement":
        return "The parties agree not to make harmful or negative public statements about each other."

    if label == "Covenant Not To Sue":
        return "One party agrees not to bring certain legal claims against the other."

    # ========================================================
    # LIABILITY
    # ========================================================

    if label == "Cap On Liability":
        cap = extract_money_cap(text)
        if cap:
            return f"The maximum financial liability is limited to {cap}."
        return "The agreement limits the maximum financial responsibility of a party."

    if label == "Uncapped Liability":
        return "Certain serious liabilities are not subject to financial limits."

    if label == "Liquidated Damages":
        return "A fixed amount must be paid if specific obligations are breached."

    # ========================================================
    # COMPETITIVE & RESTRICTIONS
    # ========================================================

    if label == "Non-Compete":
        duration = extract_duration(text)
        if duration:
            return f"The party cannot engage in competing activities for {duration}."
        return "The party is restricted from engaging in competing activities."

    if label == "No-Solicit Of Employees":
        duration = extract_duration(text)
        if duration:
            return f"The party may not solicit or hire employees for {duration}."
        return "The party may not solicit or hire employees of the other party."

    if label == "No-Solicit Of Customers":
        return "The party may not solicit customers of the other party."
    if label == "Exclusivity":
        return "One party is granted exclusive rights within a defined territory or scope."

    # ========================================================
    # ASSIGNMENT
    # ========================================================

    if label == "Anti-Assignment":
        return "The agreement cannot be transferred without prior written consent."

    if label == "Ip Ownership Assignment":
        return "The agreement defines which party owns the intellectual property."

    if label == "Joint Ip Ownership":
        return "Both parties share ownership of intellectual property."

    # ========================================================
    # LICENSE STRUCTURE
    # ========================================================

    if label == "License Grant":
        return "One party grants permission to use its software or technology under defined terms."

    if label == "Non-Transferable License":
        return "The license cannot be transferred to another party."

    if label == "Irrevocable Or Perpetual License":
        return "The license cannot be revoked and may continue indefinitely."

    if label == "Unlimited/All-You-Can-Eat-License":
        return "The agreement allows unlimited use within specified limits."

    # ========================================================
    # COMMERCIAL STRUCTURE
    # ========================================================

    if label == "Minimum Commitment":
        return "The agreement requires a minimum purchase or usage amount."

    if label == "Revenue/Profit Sharing":
        return "The parties agree to share revenue or profits."

    if label == "Price Restrictions":
        return "The agreement restricts pricing flexibility."

    if label == "Most Favored Nation":
        return "One party is guaranteed terms no worse than those offered to others."

    # ========================================================
    # COMPLIANCE & MONITORING
    # ========================================================

    if label == "Audit Rights":
        return "One party has the right to review records to verify compliance."

    if label == "Insurance":
        return "A party must maintain appropriate insurance coverage."

    # ========================================================
    # ESCROW & CONTROL
    # ========================================================

    if label == "Source Code Escrow":
        return "The source code will be held by a third party and released under specific conditions."

    if label == "Change Of Control":
        return "The agreement may be affected if ownership or control of a party changes."

    if label == "Competitive Restriction Exception":
        return "Certain competitive restrictions may not apply under specific exceptions."

    if label == "Rofr/Rofo/Rofn":
        return "One party has a right of first offer or refusal before certain transactions."

    if label == "Third Party Beneficiary":
        return "Certain third parties may have enforceable rights under this agreement."

    if label == "Warranty Duration":
        duration = extract_duration(text)
        if duration:
            return f"The warranty is valid for {duration}."
        return "The agreement provides a limited warranty."

    # ========================================================
    # DEFAULT
    # ========================================================

    return None