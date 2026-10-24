import joblib
import pandas as pd
import matplotlib.pyplot as plt

# ---- Step 1: Load the trained model and feature names ----
model = joblib.load("models/xgb_model.joblib")
feature_names = joblib.load("../data/feature_names.pkl")

# ---- Step 2: Get importance scores ----
importances = pd.Series(model.feature_importances_, index=feature_names)
importances = importances.sort_values(ascending=False)

print("=== TOP 20 FEATURES DRIVING LOAN DEFAULT PREDICTIONS ===\n")
print(importances.head(20))

# ---- Step 3: Save a bar chart of the top 15 ----
plt.figure(figsize=(10, 8))
importances.head(15).sort_values().plot(kind="barh", color="#c0392b")
plt.title("Top 15 Features Driving Loan Default Risk (XGBoost)")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("../docs/feature_importance.png")
print("\n✅ Chart saved to docs/feature_importance.png")

# ---- Step 4: Save the full importance table too ----
importances.to_csv("../docs/feature_importance.csv")
print("✅ Full table saved to docs/feature_importance.csv")