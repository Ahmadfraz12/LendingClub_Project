from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from recommendations import generate_recommendations

app = Flask(__name__)
CORS(app)

# ---- Load everything once, at startup ----
model = joblib.load("models/xgb_model.joblib")
bundle = joblib.load("models/preprocessing_bundle.joblib")
THRESHOLD = joblib.load("models/threshold.joblib")

RAW_COLUMNS = bundle["raw_input_columns"]
FINAL_FEATURES = bundle["final_feature_names"]


def preprocess_one_record(record: dict) -> pd.DataFrame:
    """Takes a dict of raw feature values (one borrower) and returns a
    one-row DataFrame with exactly the 154 columns the model expects,
    in the correct order — mirroring preprocess.py exactly."""

    df = pd.DataFrame([record])

    # emp_length -> numeric + missing flag (same logic as preprocess.py)
    emp_length_map = bundle["emp_length_map"]
    raw_emp = df.get("emp_length", pd.Series([None])).iloc[0]
    df["emp_length_numeric"] = emp_length_map.get(raw_emp, np.nan)
    df["emp_length_missing"] = int(pd.isna(df["emp_length_numeric"].iloc[0]))
    df["emp_length_numeric"] = df["emp_length_numeric"].fillna(-1)
    if "emp_length" in df.columns:
        df = df.drop(columns=["emp_length"])

    # Median-impute any missing/absent numeric columns
    for col, median_val in bundle["medians"].items():
        if col not in df.columns:
            df[col] = median_val
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(median_val)

    # One-hot encode categoricals using the SAME categories seen at training time
    for col in bundle["categorical_cols"]:
        value = df[col].iloc[0] if col in df.columns else None
        for category in bundle["categories"][col][1:]:  # drop_first=True was used in training
            dummy_col = f"{col}_{category}"
            df[dummy_col] = 1 if value == category else 0
        if col in df.columns:
            df = df.drop(columns=[col])

    # Ensure every expected final column exists, drop anything extra, fix order
    for col in FINAL_FEATURES:
        if col not in df.columns:
            df[col] = 0
    df = df[FINAL_FEATURES]

    return df


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Flask API is running"}), 200


@app.route("/api/schema", methods=["GET"])
def schema():
    """Lets the Angular frontend fetch the exact raw fields and categorical
    options needed, instead of hardcoding them twice."""
    return jsonify({
        "raw_columns": RAW_COLUMNS,
        "categorical_options": bundle["categories"],
        "numeric_defaults": bundle["medians"],
    }), 200


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        missing = [c for c in RAW_COLUMNS if c not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        X = preprocess_one_record(data)

        prob_default = float(model.predict_proba(X)[:, 1][0])
        prediction = int(prob_default >= THRESHOLD)

        result = generate_recommendations(data, prob_default)
        result["prediction"] = "Default" if prediction == 1 else "No Default"
        result["threshold_used"] = THRESHOLD
        result["disclaimer"] = (
            "Research/teaching prototype only. Not a real credit decision tool."
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)