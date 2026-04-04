def generate_explainability(applicant_data: dict, risk_prob: float):
    # applicant_data contains the engineered features AND raw features
    risk_signals = []
    positive_indicators = []
    
    # Analyze debt to income
    dti = applicant_data.get("debt_to_income", 0)
    if dti > 0.4:
        risk_signals.append(f"High debt-to-income ratio ({dti:.2f}) indicates heavy financial burden.")
    else:
        positive_indicators.append(f"Healthy debt-to-income ratio ({dti:.2f}).")
        
    # Analyze CIBIL score
    cibil = applicant_data.get("cibil_score", 0)
    if cibil < 600:
        risk_signals.append(f"Low CIBIL score ({cibil}) shows poor credit history.")
    elif cibil > 750:
        positive_indicators.append(f"Excellent CIBIL score ({cibil}) indicates high creditworthiness.")
        
    # Analyze Asset Coverage
    asset_cov = applicant_data.get("total_asset_coverage", 0)
    if asset_cov < 1.0:
        risk_signals.append(f"Low asset coverage ({asset_cov:.2f}), loan amount exceeds total declared assets.")
    elif asset_cov > 2.0:
        positive_indicators.append(f"Strong asset coverage ({asset_cov:.2f}), assets well exceed the loan amount.")
        
    term = applicant_data.get("loan_term", 0)
    if term > 240: # 20 years
        risk_signals.append(f"Long loan term ({term} months) increases default risk probability over time.")
        
    decision = "Review and Mitigate" if risk_prob > 0.5 else "Favorable"

    return {
        "risk_probability": risk_prob,
        "primary_decision_factor": "Risk Profile is elevated" if risk_prob > 0.5 else "Risk Profile is acceptable",
        "risk_signals": risk_signals,
        "positive_indicators": positive_indicators,
        "automated_decision_recommendation": decision
    }
