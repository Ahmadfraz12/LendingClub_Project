import pandas as pd
import os

DATA_PATH = "../data/cleaned_lending_club.csv"

# ---- Step 1: File size ----
size_mb = os.path.getsize(DATA_PATH) / (1024 * 1024)
print(f"File size: {size_mb:.1f} MB")

# ---- Step 2: Count rows without loading everything into memory ----
row_count = 0
for chunk in pd.read_csv(DATA_PATH, chunksize=100_000):
    row_count += len(chunk)
print(f"Total rows: {row_count:,}")

# ---- Step 3: Peek at columns and types using just the first few rows ----
sample = pd.read_csv(DATA_PATH, nrows=5)
print(f"\nNumber of columns: {sample.shape[1]}")
print("\nColumn names and types:")
print(sample.dtypes)

print("\nFirst 3 rows:")
print(sample.head(3))

# ---- Step 4: Look for likely target columns ----
likely_targets = [c for c in sample.columns if "status" in c.lower() or "default" in c.lower() or "loan_status" in c.lower()]
print("\nLikely target column(s):", likely_targets)