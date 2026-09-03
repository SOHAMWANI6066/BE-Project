import pandas as pd

df = pd.read_csv("data/processed/train_full.csv")

labels = sorted(df["label"].unique())

print("\nLabel Order:\n")
for i, label in enumerate(labels):
    print(i, label)