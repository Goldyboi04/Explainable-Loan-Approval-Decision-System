import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from xgboost import XGBClassifier

# ----------------------------
# Load and clean dataset
# ----------------------------
df = pd.read_csv("loan_approval_dataset.csv")

df.columns = df.columns.str.strip()
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

df.drop("loan_id", axis=1, inplace=True)

# ----------------------------
# Feature engineering
# ----------------------------
df["debt_to_income"] = df["loan_amount"] / (df["income_annum"] + 1)

X = df.drop("loan_status", axis=1)
y = df["loan_status"].map({"Approved": 1, "Rejected": 0})

categorical_cols = ["education", "self_employed"]
numerical_cols = [c for c in X.columns if c not in categorical_cols]

# ----------------------------
# Train-test split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================
# Logistic Regression Pipeline
# ============================
log_preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(drop="first"), categorical_cols),
    ("num", StandardScaler(), numerical_cols)
])

log_model = Pipeline([
    ("preprocess", log_preprocessor),
    ("model", LogisticRegression(
        max_iter=1000,
        C=0.5,
        solver="lbfgs"
    ))
])

log_model.fit(X_train, y_train)

pickle.dump(log_model, open("loan_model_logistic.pkl", "wb"))

# ============================
# XGBoost Pipeline
# ============================
xgb_preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numerical_cols)
])

xgb_model = Pipeline([
    ("preprocess", xgb_preprocessor),
    ("model", XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        reg_lambda=1.0,
        eval_metric="logloss",
        random_state=42
    ))
])

xgb_model.fit(X_train, y_train)

pickle.dump(xgb_model, open("loan_model_xgboost.pkl", "wb"))

print("Models saved:")
print("- loan_model_logistic.pkl")
print("- loan_model_xgboost.pkl")

