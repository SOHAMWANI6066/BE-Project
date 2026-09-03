import pandas as pd

INPUT = "hybrid/results/active_learning_candidates.csv"
OUTPUT = "hybrid/results/active_learning_to_label.csv"

# Number of samples to label
N = 40

df = pd.read_csv(INPUT)

# Already sorted by priority_score
label_df = df.head(N)

label_df.to_csv(OUTPUT, index=False)

print(f"✅ Selected top {N} clauses for manual labeling")
print(f"📁 File saved to: {OUTPUT}")
