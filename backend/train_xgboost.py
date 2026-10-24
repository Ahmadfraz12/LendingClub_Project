import joblib
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)

# ---- Step 1: Load preprocessed data ----
X_train = joblib.load("../data/X_train.pkl")
X_test = joblib.load("../data/X_test.pkl")
y_train = joblib.load("../data/y_train.pkl")
y_test = joblib.load("../data/y_test.pkl")

print("Data loaded. Training samples:", X_train.shape[0])

# ---- Step 2: Calculate class weight to counter the 80/20 imbalance ----
n_negative = (y_train == 0).sum()
n_positive = (y_train == 1).sum()
scale_pos_weight = n_negative / n_positive
print(f"\nClass counts - No Default: {n_negative}, Default: {n_positive}")
print(f"scale_pos_weight = {scale_pos_weight:.3f}")

# ---- Step 3: Train XGBoost WITH class weighting ----
model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,   # back to the computed 4.009
    random_state=42,
    n_jobs=-1
)

print("\nTraining XGBoost with class weighting... (this may take a few minutes)")
model.fit(X_train, y_train)
print("Training complete!")

# ---- Step 4: Get predicted probabilities ----
y_pred_probs = model.predict_proba(X_test)[:, 1]

# ---- Step 5: Apply your 0.55 threshold ----
THRESHOLD = 0.55
y_pred = (y_pred_probs >= THRESHOLD).astype(int)

# ---- Step 6: Metrics ----
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_probs)

print(f"\n=== XGBOOST METRICS (threshold = {THRESHOLD}, class-weighted) ===")
print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"AUC-ROC:   {auc:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["No Default", "Default"]))

# ---- Step 7: Save ----
joblib.dump(model, "models/xgb_model.joblib")
joblib.dump(y_pred, "../data/y_pred.pkl")
joblib.dump(y_pred_probs, "../data/y_pred_probs.pkl")
joblib.dump(THRESHOLD, "models/threshold.joblib")

print(f"\n✅ Model and threshold ({THRESHOLD}) saved to models/")