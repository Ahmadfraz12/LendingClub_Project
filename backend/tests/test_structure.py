import joblib
import os

def test_model_file_exists():
    assert os.path.exists("backend/models/xgb_model.joblib")

def test_preprocessing_bundle_exists():
    assert os.path.exists("backend/models/preprocessing_bundle.joblib")

def test_threshold_exists():
    assert os.path.exists("backend/models/threshold.joblib")

def test_model_loads_and_predicts():
    model = joblib.load("backend/models/xgb_model.joblib")
    bundle = joblib.load("backend/models/preprocessing_bundle.joblib")
    threshold = joblib.load("backend/models/threshold.joblib")

    assert hasattr(model, "predict_proba")
    assert 0 < threshold < 1
    assert len(bundle["final_feature_names"]) > 0

    # Build a dummy row of zeros matching the expected feature count,
    # just to confirm the model will accept the right shape
    import pandas as pd
    dummy = pd.DataFrame([[0] * len(bundle["final_feature_names"])],
                          columns=bundle["final_feature_names"])
    prob = model.predict_proba(dummy)[:, 1][0]
    assert 0 <= prob <= 1