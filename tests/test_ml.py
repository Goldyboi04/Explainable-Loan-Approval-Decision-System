import pytest
import pandas as pd
from ml.explainability import generate_explainability
from ml.train_model import engineer_features

def test_generate_explainability_high_risk():
    data = {
        "debt_to_income": 0.6,
        "cibil_score": 550,
        "total_asset_coverage": 0.8,
        "loan_term": 360
    }
    risk_prob = 0.8
    result = generate_explainability(data, risk_prob)
    
    assert result["risk_probability"] == 0.8
    assert "High debt-to-income ratio" in str(result["risk_signals"])
    assert "Low CIBIL score" in str(result["risk_signals"])
    assert "Low asset coverage" in str(result["risk_signals"])
    assert result["automated_decision_recommendation"] == "Review and Mitigate"

def test_generate_explainability_low_risk():
    data = {
        "debt_to_income": 0.2,
        "cibil_score": 800,
        "total_asset_coverage": 3.0,
        "loan_term": 120
    }
    risk_prob = 0.1
    result = generate_explainability(data, risk_prob)
    
    assert result["risk_probability"] == 0.1
    assert "Healthy debt-to-income ratio" in str(result["positive_indicators"])
    assert "Excellent CIBIL score" in str(result["positive_indicators"])
    assert "Strong asset coverage" in str(result["positive_indicators"])
    assert result["automated_decision_recommendation"] == "Favorable"

def test_engineer_features():
    df = pd.DataFrame([{
        "income_annum": 100000,
        "loan_amount": 50000,
        "residential_assets_value": 100000,
        "commercial_assets_value": 0,
        "luxury_assets_value": 0,
        "bank_asset_value": 50000,
    }])
    
    engineered = engineer_features(df)
    
    assert engineered["debt_to_income"].iloc[0] == 0.5
    assert engineered["loan_to_assets"].iloc[0] == 50000 / 150000
    assert engineered["total_asset_coverage"].iloc[0] == 150000 / 50000
