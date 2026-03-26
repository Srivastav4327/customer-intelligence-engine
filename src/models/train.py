import json
import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

FEATURES = [
    "Frequency",
    "Monetary",
    "customer_lifespan",
    "total_transactions",
    "avg_order_value",
    "max_order_value",
]

# --- Load data ---
df = pd.read_csv("data/processed/rfm.csv")
df["churn"] = df["Recency"].apply(lambda x: 1 if x > 90 else 0)
print(df["churn"].value_counts())

X = df[FEATURES]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Load tuned hyperparameters from Optuna if available ---
BEST_PARAMS_PATH = "src/models/best_params.json"
DEFAULT_PARAMS = {
    "n_estimators": 200,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
}

if os.path.exists(BEST_PARAMS_PATH):
    with open(BEST_PARAMS_PATH) as f:
        params = json.load(f)
    print(f"Loaded Optuna best params from {BEST_PARAMS_PATH}")
else:
    params = DEFAULT_PARAMS
    print("No best_params.json found, using default hyperparameters.")

# --- Train model ---
model = XGBClassifier(**params, random_state=42, eval_metric="logloss")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))

importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_,
}).sort_values(by="importance", ascending=False)
print(importance)

# --- Save predictions and model ---
df["prediction"] = model.predict(X)
df["prediction_probability"] = model.predict_proba(X)[:, 1]
df.to_csv("data/processed/churn_predictions.csv", index=False)

joblib.dump(model, "src/models/churn_model.pkl")
print("Saved trained model to src/models/churn_model.pkl")
