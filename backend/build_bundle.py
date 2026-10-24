import pandas as pd
import numpy as np
import joblib

DATA_PATH = "../data/cleaned_lending_club.csv"

df = pd.read_csv(DATA_PATH)

high_missing_cols = [
    "inq_last_12m", "total_cu_tl", "open_acc_6m", "open_act_il", "inq_fi",
    "max_bal_bc", "open_rv_24m", "open_il_12m", "total_bal_il", "open_rv_12m",
    "open_il_24m"
]
df = df.drop(columns=high_missing_cols)

emp_length_map = {
    "< 1 year": 0, "1 year": 1, "2 years": 2, "3 years": 3, "4 years": 4,
    "5 years": 5, "6 years": 6, "7 years": 7, "8 years": 8, "9 years": 9,
    "10+ years": 10
}

X = df.drop(columns=["default"])
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(include="object").columns.tolist()
categorical_cols = [c for c in categorical_cols if c != "emp_length"]

# Medians for imputing missing numeric values at prediction time
medians = X[numeric_cols].median().to_dict()

# Exact categories seen during training, per categorical column (needed to
# rebuild identical one-hot columns at prediction time, in the same order)
categories = {col: sorted(X[col].dropna().unique().tolist()) for col in categorical_cols}

final_feature_names = joblib.load("../data/feature_names.pkl")

bundle = {
    "high_missing_cols": high_missing_cols,
    "emp_length_map": emp_length_map,
    "numeric_cols": numeric_cols,      # includes emp_length_numeric name but computed separately
    "categorical_cols": categorical_cols,
    "medians": medians,
    "categories": categories,
    "final_feature_names": final_feature_names,
    "raw_input_columns": [c for c in df.columns if c not in ("default",)],
}

joblib.dump(bundle, "models/preprocessing_bundle.joblib")
print("✅ Saved models/preprocessing_bundle.joblib")
print(f"\nRaw input columns needed from the form ({len(bundle['raw_input_columns'])}):")
for c in bundle["raw_input_columns"]:
    print(" -", c)