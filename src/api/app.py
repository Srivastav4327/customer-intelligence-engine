from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Customer Intelligence API")

# Load the Optuna-optimized model; fall back to base model if not found
OPTIMIZED_MODEL = Path("src/models/churn_model_optimized.pkl")
BASE_MODEL = Path("src/models/churn_model.pkl")
model_path = OPTIMIZED_MODEL if OPTIMIZED_MODEL.exists() else BASE_MODEL
model = joblib.load(model_path)
print(f"Loaded model from: {model_path}")


class CustomerData(BaseModel):
    frequency: float
    monetary: float
    customer_lifespan: float
    total_transactions: float
    avg_order_value: float
    max_order_value: float


@app.get("/")
def home():
    return {
        "message": "Customer Intelligence API Running",
        "model": str(model_path),
    }


@app.post("/predict_churn")
def predict_churn(data: CustomerData):
    features = np.array([[
        data.frequency,
        data.monetary,
        data.customer_lifespan,
        data.total_transactions,
        data.avg_order_value,
        data.max_order_value,
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4),
        "risk_level": "High" if probability >= 0.7 else "Medium" if probability >= 0.4 else "Low",
    }
