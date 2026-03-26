import os
import pandas as pd


def advanced_features(df):
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    features = df.groupby("Customer ID").agg({
        "InvoiceDate": [
            lambda x: (x.max() - x.min()).days,
            "count"
        ],
        "TotalPrice": ["mean", "max"]
    })

    features.columns = [
        "customer_lifespan",
        "total_transactions",
        "avg_order_value",
        "max_order_value"
    ]

    return features.reset_index()


def build_rfm():
    # Use absolute path for the cleaned CSV file
    cleaned_data_path = os.path.join(os.path.dirname(__file__), '../../data/processed/cleaned.csv')
    df = pd.read_csv(cleaned_data_path)

    # Ensure InvoiceDate is in datetime format
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Set snapshot_date to the maximum InvoiceDate
    snapshot_date = df['InvoiceDate'].max()

    # Build RFM table
    rfm = df.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "Invoice": "nunique",
        "TotalPrice": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    # Merge in advanced customer-level features
    rfm = rfm.reset_index()
    advanced = advanced_features(df.copy())
    rfm = rfm.merge(advanced, on="Customer ID", how="left")

    # Save to CSV
    rfm_data_path = os.path.join(os.path.dirname(__file__), '../../data/processed/rfm.csv')
    rfm.to_csv(rfm_data_path, index=False)

if __name__ == "__main__":
    build_rfm()
    print("RFM created!")
