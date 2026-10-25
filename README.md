# LendingClub Loan Default Predictor

A full-stack machine learning application that predicts loan default risk using an XGBoost model trained on 1.3M+ LendingClub loan records, with a Flask REST API backend and Angular frontend.

## Project Overview

- **Dataset:** LendingClub cleaned loan data — 1,345,310 rows, 61 original columns (50 features used after cleaning, 154 after one-hot encoding)
- **Target:** Binary `default` column (1 = defaulted, 0 = did not default)
- **Class balance:** 80% no default / 20% default (imbalanced)
- **Model:** XGBoost Classifier, with `scale_pos_weight=4.009` to address class imbalance
- **Decision threshold:** 0.55 (instead of the default 0.5) — a borrower is classified as "high risk of default" only when the model's predicted probability is ≥ 55%

## Model Performance (on 20% held-out test set, 269,062 rows)

| Metric | Score |
|---|---|
| Accuracy | 70.74% |
| Precision | 35.80% |
| Recall | 58.69% |
| F1 Score | 0.4447 |
| AUC-ROC | 0.7309 |

**Note on accuracy vs. recall tradeoff:** Raw accuracy is a misleading metric here due to class imbalance (a model predicting "no default" for every loan would already score ~80% accuracy while being useless). We prioritized Recall over Precision via class weighting, since in a lending context, missing a real defaulter is typically costlier than over-flagging a safe borrower. This is a deliberate design choice, not an unoptimized result — see `docs/` for the full comparison of weighting strategies tested.

## Top Features Driving Default Risk

Based on XGBoost feature importance (see `docs/feature_importance.csv` and `.png`):
1. Interest rate
2. Loan grade (B, C)
3. Loan term (60 months)
4. Sub-grade
5. Home ownership status

**Important caveat:** Interest rate and grade are themselves outputs of LendingClub's own internal risk assessment (based on FICO, DTI, and credit history at origination) — not independent borrower actions. Our recommendation engine (`backend/recommendations.py`) deliberately targets the *underlying* actionable factors (DTI, FICO, recent credit activity, loan term, employment length) rather than these derived outputs, since a borrower cannot directly "fix" their assigned grade.

## Architecture
Browser / Angular form (localhost:4200)
|
| POST /api/predict (JSON)
v
Angular dev proxy -> Flask API (127.0.0.1:5000)
|
| preprocessing -> XGBoost model -> 0.55 threshold
v
JSON prediction + recommendations -> Angular result panel

Git repository -> GitHub Actions (backend structure tests + Angular build)
-> GitHub Pages (static Angular frontend ONLY)

**Important:** GitHub Pages hosts only the static Angular interface. It cannot run Python or the XGBoost model. Real predictions require Flask running locally. The deployed Pages site clearly discloses this limitation in its UI.

## Project Structure
LendingClub_Project/
├── .github/workflows/ # CI (backend tests + frontend build) and Pages deployment
├── backend/
│ ├── app.py # Flask REST API
│ ├── preprocess.py # Full-dataset preprocessing (training time)
│ ├── build_bundle.py # Builds the preprocessing bundle Flask uses at inference
│ ├── train_xgboost.py # Model training with class weighting
│ ├── feature_importance.py # Feature importance analysis
│ ├── feature_direction.py # Risk direction analysis (for recommendations)
│ ├── recommendations.py # Borrower-facing recommendation engine
│ ├── models/ # Trained model, preprocessing bundle, threshold
│ ├── tests/ # pytest suites (live API tests + CI structure tests)
│ └── requirements.txt / requirements-ci.txt
├── frontend/ # Angular application
├── docs/ # Feature importance chart and table
└── data/ # Excluded from Git (397MB+ dataset, regenerable .pkl files)

## Setup Instructions

### Backend
```powershell
cd backend
python -m venv ../.venv
../.venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```powershell
cd frontend
npm install
ng serve --open --proxy-config proxy.conf.json
```

Visit `http://localhost:4200`.

## Live Demo (Static Only)

https://ahmadfraz12.github.io/LendingClub_Project/

This shows the UI only — predictions require running the backend locally as described above.

## Disclaimer

This is a research/teaching prototype. It is not a real credit decision tool and should not be used for actual lending decisions.