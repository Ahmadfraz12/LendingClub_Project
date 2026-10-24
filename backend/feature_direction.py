import pandas as pd
import joblib

# ---- Step 1: Reload original data just for the key numeric columns + target ----
df = pd.read_csv("../data/cleaned_lending_club.csv", usecols=[
    "int_rate", "mort_acc", "acc_open_past_24mths", "emp_length",
    "fico_range_low", "funded_amnt", "dti", "default"
])

# ---- Step 2: Compare average values between defaulters and non-defaulters ----
print("=== AVERAGE VALUE BY OUTCOME (Default=1 vs No Default=0) ===\n")
comparison = df.groupby("default")[
    ["int_rate", "mort_acc", "acc_open_past_24mths", "fico_range_low", "funded_amnt", "dti"]
].mean()
print(comparison)

print("\n=== DIRECTION (Default avg - No Default avg) ===")
direction = comparison.loc[1] - comparison.loc[0]
print(direction)
print("\nPositive = higher in defaulters (risk increases with higher values)")
print("Negative = lower in defaulters (risk increases with lower values)")

# ---- Step 3: emp_length direction (categorical) ----
print("\n=== DEFAULT RATE BY EMPLOYMENT LENGTH ===")
print(df.groupby("emp_length")["default"].mean().sort_values(ascending=False))

# ---- Step 4: Grade/term/purpose default rates (reload those columns too) ----
df2 = pd.read_csv("../data/cleaned_lending_club.csv", usecols=["grade", "term", "purpose", "home_ownership", "default"])
print("\n=== DEFAULT RATE BY GRADE ===")
print(df2.groupby("grade")["default"].mean().sort_values(ascending=False))
print("\n=== DEFAULT RATE BY TERM ===")
print(df2.groupby("term")["default"].mean())
print("\n=== DEFAULT RATE BY PURPOSE ===")
print(df2.groupby("purpose")["default"].mean().sort_values(ascending=False))
print("\n=== DEFAULT RATE BY HOME OWNERSHIP ===")
print(df2.groupby("home_ownership")["default"].mean().sort_values(ascending=False))