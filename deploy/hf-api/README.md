---
title: Customer Churn API
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8000
pinned: false
---

# Customer Churn Prediction API

A FastAPI service that predicts customer churn probability using an XGBoost model
optimised with Optuna hyperparameter tuning.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check + model version |
| GET | `/docs` | Interactive Swagger UI |
| POST | `/predict_churn` | Predict churn for a customer |

## Example Request

```bash
curl -X POST "https://<your-space-url>/predict_churn" \
  -H "Content-Type: application/json" \
  -d '{
    "frequency": 12,
    "monetary": 8500,
    "customer_lifespan": 365,
    "total_transactions": 12,
    "avg_order_value": 708.33,
    "max_order_value": 1500
  }'
```

## Example Response

```json
{
  "churn_prediction": 1,
  "churn_probability": 0.5765,
  "risk_level": "Medium"
}
```
