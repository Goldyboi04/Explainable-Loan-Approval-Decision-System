from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pickle
import pandas as pd
import os

from . import models, schemas
from .database import engine, get_db

from ml.explainability import generate_explainability
from ml.train_model import engineer_features

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Credit Risk API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Preload model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "..", "ml", "loan_model_xgboost.pkl")
with open(model_path, "rb") as f:
    xgb_model = pickle.load(f)

@app.post("/predict", response_model=schemas.PredictionResponse)
def predict_credit_risk(applicant: schemas.ApplicantCreate, db: Session = Depends(get_db)):
    # 1. Transform input to DataFrame
    df_input = pd.DataFrame([applicant.model_dump()])
    
    # 2. Engineer features
    df_engineered = engineer_features(df_input)
    
    # Get values for explainability
    applicant_data_dict = df_engineered.iloc[0].to_dict()
    
    # 3. Model Prediction
    try:
        # predict_proba returns [[prob_0, prob_1]]
        # Cast to float, as np.float32 may not be supported by the DB driver natively
        risk_prob = float(xgb_model.predict_proba(df_engineered)[0][1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # 4. Generate Explainability
    explanation = generate_explainability(applicant_data_dict, risk_prob)
    
    # 5. Save to Database
    db_record = models.ApplicantRecord(
        **applicant.model_dump(),
        debt_to_income=float(applicant_data_dict.get("debt_to_income", 0)),
        loan_to_assets=float(applicant_data_dict.get("loan_to_assets", 0)),
        total_asset_coverage=float(applicant_data_dict.get("total_asset_coverage", 0)),
        risk_probability=explanation["risk_probability"],
        automated_decision=explanation["automated_decision_recommendation"],
        explainability_json=explanation
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return explanation

@app.get("/predictions", response_model=list[schemas.ApplicantResponse])
def get_predictions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    records = db.query(models.ApplicantRecord).offset(skip).limit(limit).all()
    return records
