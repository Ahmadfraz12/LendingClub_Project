import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import joblib

DATA_PATH = "../data/cleaned_lending_club.csv"

# ---- Step 1: Load ----
df = pd.read_csv(DATA_PATH)
print("Original shape:", df.shape)

# ---- Step 2: Drop columns with too much missing data (~60%) ----
high_missing_cols = [
    "inq_last_12m", "total_cu_tl", "open_acc_6m", "open_act_il", "inq_fi",
    "max_bal_bc", "open_rv_24m", "open_il_12m", "total_bal_il", "open_rv_12m",
    "open_il_24m"
]
df = df.drop(columns=high_missing_cols)
print("Shape after dropping high-missing columns:", df.shape)

# ---- Step 3: Handle emp_length (ordinal, with missing as its own category) ----
emp_length_map = {
    "< 1 year": 0, "1 year": 1, "2 years": 2, "3 years": 3, "4 years": 4,
    "5 years": 5, "6 years": 6, "7 years": 7, "8 years": 8, "9 years": 9,
    "10+ years": 10
}
df["emp_length_numeric"] = df["emp_length"].map(emp_length_map)
df["emp_length_missing"] = df["emp_length_numeric"].isnull().astype(int)
df["emp_length_numeric"] = df["emp_length_numeric"].fillna(-1)  # -1 = flagged separately by emp_length_missing
df = df.drop(columns=["emp_length"])

# ---- Step 4: Separate target ----
y = df["default"]
X = df.drop(columns=["default"])

# ---- Step 5: Median-impute remaining numeric columns ----
numeric_cols = X.select_dtypes(include=[np.number]).columns
print(f"\nImputing {X[numeric_cols].isnull().sum().sum()} total missing numeric values with column medians...")
X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].median())

# ---- Step 6: One-hot encode categorical columns ----
categorical_cols = X.select_dtypes(include="object").columns.tolist()
print("\nOne-hot encoding:", categorical_cols)
X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

print("\nFinal feature count:", X.shape[1])
print("Any remaining missing values?", X.isnull().sum().sum())

# ---- Step 7: Train/test split (80/20) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("\nTraining set:", X_train.shape)
print("Testing set:", X_test.shape)

# ---- Step 8: Save everything ----
joblib.dump(X_train, "../data/X_train.pkl")
joblib.dump(X_test, "../data/X_test.pkl")
joblib.dump(y_train, "../data/y_train.pkl")
joblib.dump(y_test, "../data/y_test.pkl")
joblib.dump(list(X.columns), "../data/feature_names.pkl")

print("\n✅ Preprocessing done. Files saved in data/.")