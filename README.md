# Customer Intelligence Engine

An end-to-end customer analytics platform featuring RFM segmentation, churn prediction with XGBoost, and an interactive Streamlit dashboard — all deployed to the cloud.

## Key Insights

- Revenue shows consistent monthly growth
- Customer retention decreases after initial purchase
- High-value customers contribute majority of revenue
- Majority customers fall under low-value segment

## Technical Highlights

- Optimized XGBoost hyperparameters using Optuna to maximize ROC-AUC
- FastAPI REST endpoint for real-time churn predictions with risk levels (High / Medium / Low)
- Streamlit dashboard for interactive customer segmentation and churn visualization
- Containerized with Docker; deployed to Hugging Face Spaces (API) and Streamlit Community Cloud (Dashboard)

## Project Structure

```
├── dashboard/          # Streamlit dashboard
├── src/
│   ├── api/            # FastAPI app
│   ├── models/         # Training & Optuna tuning scripts
│   ├── features/       # Feature engineering
│   └── data_pipeline/  # Ingestion & cleaning
├── sql/                # Cohort, retention, and segmentation queries
├── deploy/hf-api/      # Hugging Face Space deployment files
├── Dockerfile.api
├── Dockerfile.dashboard
└── docker-compose.yml
```

## Local Setup

```bash
# Install dependencies
pip install -r requirements-api.txt       # API only
pip install -r requirements-dashboard.txt # Dashboard only

# Run API
uvicorn src.api.app:app --reload

# Run Dashboard
streamlit run dashboard/app.py
```

## Local Docker

```bash
# Build and run both services
docker compose up --build

# API → http://localhost:8000/docs
# Dashboard → http://localhost:8501
```

## Cloud Deployment

### FastAPI → Hugging Face Spaces

See `deploy/hf-api/` — push its contents to a new HF Docker Space.

> Live API: _[Add your HF Space URL here]_

### Streamlit Dashboard → Streamlit Community Cloud

Connect your GitHub repo at https://share.streamlit.io  
Set **Main file**: `dashboard/app.py`

> Live Dashboard: _[Add your Streamlit Cloud URL here]_

## Resume Bullet

> *"Developed an end-to-end Customer Intelligence Engine with XGBoost churn prediction (ROC-AUC ~0.80, optimized via Optuna), deployed a FastAPI scoring endpoint to Hugging Face Spaces and an interactive Streamlit dashboard to Streamlit Community Cloud using Docker."*
