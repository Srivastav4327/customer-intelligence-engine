import json
import pandas as pd
import optuna
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
import joblib

FEATURES = [
    "Frequency",
    "Monetary",
    "customer_lifespan",
    "total_transactions",
    "avg_order_value",
    "max_order_value",
]


def load_data():
    df = pd.read_csv("data/processed/rfm.csv")
    df["churn"] = df["Recency"].apply(lambda x: 1 if x > 90 else 0)
    return df[FEATURES], df["churn"]


def objective(trial):
    X, y = load_data()

    param = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "random_state": 42,
        "eval_metric": "logloss",
    }

    model = XGBClassifier(**param)
    score = cross_val_score(model, X, y, cv=3, scoring="roc_auc").mean()
    return score


if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)

    print("\nBest parameters:")
    print(study.best_params)
    print(f"Best ROC-AUC: {study.best_value:.4f}")

    # Save best params to JSON so train.py can reuse them
    with open("src/models/best_params.json", "w") as f:
        json.dump(study.best_params, f, indent=4)
    print("Saved best params to src/models/best_params.json")

    # Train and save the final optimized model on all data
    X, y = load_data()
    best_model = XGBClassifier(**study.best_params, random_state=42, eval_metric="logloss")
    best_model.fit(X, y)

    joblib.dump(best_model, "src/models/churn_model_optimized.pkl")
    print("Saved optimized model to src/models/churn_model_optimized.pkl")
