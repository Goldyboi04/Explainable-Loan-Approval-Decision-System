from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from datetime import datetime
from .database import Base

class ApplicantRecord(Base):
    __tablename__ = "applicant_records"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Input features
    no_of_dependents = Column(Integer)
    education = Column(String)
    self_employed = Column(String)
    income_annum = Column(Float)
    loan_amount = Column(Float)
    loan_term = Column(Integer)
    cibil_score = Column(Float)
    residential_assets_value = Column(Float)
    commercial_assets_value = Column(Float)
    luxury_assets_value = Column(Float)
    bank_asset_value = Column(Float)
    
    # Engineered features / Ratios
    debt_to_income = Column(Float)
    loan_to_assets = Column(Float)
    total_asset_coverage = Column(Float)
    
    # Explainable ML Outputs
    risk_probability = Column(Float)
    automated_decision = Column(String)
    explainability_json = Column(JSON)
