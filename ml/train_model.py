import pandas as pd
import pickle
import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, precision_score
from xgboost import XGBClassifier

def engineer_features(df):
    df = df.copy()
    # Handle division by zero
    df["income_annum"] = df["income_annum"].replace(0, 1)
    df["loan_amount"] = df["loan_amount"].replace(0, 1)
    
    # Financial Ratios
    df["debt_to_income"] = df["loan_amount"] / df["income_annum"]
    
    df["total_assets"] = (
        df["residential_assets_value"] + 
        df["commercial_assets_value"] + 
        df["luxury_assets_value"] + 
        df["bank_asset_value"]
    )
    df["total_assets"] = df["total_assets"].replace(0, 1) # Avoid div by zero
    
    df["loan_to_assets"] = df["loan_amount"] / df["total_assets"]
    df["total_asset_coverage"] = df["total_assets"] / df["loan_amount"]
    
    # Drop intermediate columns if we only want the ratios or keep them.
    # We will keep them for the model to learn better.
    df.drop(columns=["total_assets"], inplace=True)
    return df


def preprocess_data(csv_path="loan_approval_dataset.csv"):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    if "loan_id" in df.columns:
        df.drop("loan_id", axis=1, inplace=True)

    df = engineer_features(df)

    X = df.drop("loan_status", axis=1)
    # Reframing as Risk Assessment: Rejected = 1 (Risk), Approved = 0 (No Risk)
    y = df["loan_status"].map({"Approved": 0, "Rejected": 1})

    return X, y

def train_and_evaluate():
    # Adjust path assuming script might be called from project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "loan_approval_dataset.csv")
    
    X, y = preprocess_data(csv_path)
    categorical_cols = ["education", "self_employed"]
    numerical_cols = [c for c in X.columns if c not in categorical_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    log_preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(drop="first"), categorical_cols),
        ("num", StandardScaler(), numerical_cols)
    ])

    log_model = Pipeline([
        ("preprocess", log_preprocessor),
        ("model", LogisticRegression(max_iter=1000, C=0.5, solver="lbfgs", class_weight="balanced"))
    ])
    log_model.fit(X_train, y_train)

    xgb_preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numerical_cols)
    ])

    xgb_model = Pipeline([
        ("preprocess", xgb_preprocessor),
        ("model", XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=3,
            reg_lambda=1.0,
            scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),  # Handle imbalance
            eval_metric="logloss",
            random_state=42
        ))
    ])
    xgb_model.fit(X_train, y_train)

    print("--- Logistic Regression ---")
    y_pred_log = log_model.predict(X_test)
    print(classification_report(y_test, y_pred_log))
    print(f"Logistic Regression Precision (Risk=1): {precision_score(y_test, y_pred_log):.2f}")

    print("--- XGBoost ---")
    y_pred_xgb = xgb_model.predict(X_test)
    print(classification_report(y_test, y_pred_xgb))
    print(f"XGBoost Precision (Risk=1): {precision_score(y_test, y_pred_xgb):.2f}")

    # Save models in ml/ directory
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    pickle.dump(log_model, open(os.path.join(ml_dir, "loan_model_logistic.pkl"), "wb"))
    pickle.dump(xgb_model, open(os.path.join(ml_dir, "loan_model_xgboost.pkl"), "wb"))
    print("Models saved successfully in ml/ directory.")

if __name__ == "__main__":
    train_and_evaluate()
