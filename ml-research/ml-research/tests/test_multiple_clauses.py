from pipeline.analyze_clause import analyze_clause

clauses = [

    # 1️⃣ Governing law + jurisdiction (medium risk, rule-based simplify)
    "This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to conflict of law principles.",

    # 2️⃣ Termination with condition (high risk, simplify)
    "Either party may terminate this Agreement immediately upon written notice if the other party commits a material breach and fails to cure such breach within fifteen days.",

    # 3️⃣ Confidentiality obligation (medium risk, short clause)
    "Each party agrees to keep all confidential information strictly confidential.",

    # 4️⃣ Indemnification (high risk, complex)
    "The Supplier shall indemnify, defend, and hold harmless the Company from and against any and all claims, damages, losses, liabilities, and expenses arising out of Supplier’s negligence.",

    # 5️⃣ Limitation of liability (very high risk)
    "In no event shall either party be liable for any indirect, incidental, or consequential damages, even if advised of the possibility of such damages.",

    # 6️⃣ Non-compete clause (high risk)
    "The Employee shall not engage in any competing business activities for a period of two years following termination of employment.",

    # 7️⃣ Audit rights (medium risk)
    "The Company reserves the right to audit the financial records of the Vendor upon reasonable notice.",

    # 8️⃣ Very short / ambiguous clause (edge case)
    "Force majeure.",

    # 9️⃣ Long procedural clause (should not over-simplify)
    "All notices under this Agreement shall be in writing and shall be deemed given when delivered personally or sent by registered mail to the address of the receiving party.",

    # 🔟 Weird but real-world clause (stress test)
    "Nothing herein shall be construed as creating a partnership, joint venture, or agency relationship between the parties."
]

for i, c in enumerate(clauses, 1):
    print(f"\n--- Clause {i} ---")
    result = analyze_clause(c)
    print("Type:", result["clause_type"])
    print("Risk:", result["risk_level"])
    print("Simplified:", result["simplified_text"])