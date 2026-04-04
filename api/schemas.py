from pydantic import BaseModel
from typing import List, Optional

class ApplicantCreate(BaseModel):
    no_of_dependents: int
    education: str
    self_employed: str
    income_annum: float
    loan_amount: float
    loan_term: int
    cibil_score: float
    residential_assets_value: float
    commercial_assets_value: float
    luxury_assets_value: float
    bank_asset_value: float

class PredictionResponse(BaseModel):
    risk_probability: float
    primary_decision_factor: str
    risk_signals: List[str]
    positive_indicators: List[str]
    automated_decision_recommendation: str

class ApplicantResponse(BaseModel):
    id: int
    no_of_dependents: int
    income_annum: float
    loan_amount: float
    cibil_score: float
    debt_to_income: float
    risk_probability: float
    automated_decision: str
    explainability_json: dict

    class Config:
        from_attributes = True
