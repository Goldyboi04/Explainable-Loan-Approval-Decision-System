def test_predict_endpoint(client):
    payload = {
        "no_of_dependents": 2,
        "education": "Graduate",
        "self_employed": "No",
        "income_annum": 500000,
        "loan_amount": 2000000,
        "loan_term": 120,
        "cibil_score": 750,
        "residential_assets_value": 1500000,
        "commercial_assets_value": 500000,
        "luxury_assets_value": 0,
        "bank_asset_value": 100000
    }
    
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_probability" in data
    assert "automated_decision_recommendation" in data
    assert "risk_signals" in data
    assert "positive_indicators" in data
    
def test_get_predictions_endpoint(client):
    response = client.get("/predictions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0 # Given we just inserted one in the predict test
