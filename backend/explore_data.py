import pandas as pd

DATA_PATH = "../data/cleaned_lending_club.csv"

# ---- Step 1: Load the full dataset ----
# (1.3M rows x 61 columns should still fit comfortably in memory on most machines)
df = pd.read_csv(DATA_PATH)
print("Shape:", df.shape)

# ---- Step 2: Target column balance ----
print("\n=== TARGET: default ===")
print(df["default"].value_counts())
print(df["default"].value_counts(normalize=True) * 100)

# ---- Step 3: All column names, in order ----
print("\n=== ALL COLUMNS ===")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}  ({df[col].dtype})")

# ---- Step 4: Missing values ----
print("\n=== MISSING VALUES (columns with any) ===")
missing = df.isnull().sum()
print(missing[missing > 0].sort_values(ascending=False))

# ---- Step 5: Non-numeric (text/categorical) columns ----
text_cols = df.select_dtypes(include="object").columns.tolist()
print("\n=== TEXT / CATEGORICAL COLUMNS ===")
print(text_cols)
for col in text_cols:
    n_unique = df[col].nunique()
    print(f"\n{col}: {n_unique} unique values")
    if n_unique <= 15:
        print(df[col].value_counts())