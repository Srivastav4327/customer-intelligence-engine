import os
import pandas as pd

def clean_data():
    # Use absolute path for the CSV file
    raw_data_path = os.path.join(os.path.dirname(__file__), '../../data/raw/combined.csv')
    df = pd.read_csv(raw_data_path)
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove missing customers
    df = df.dropna(subset=["Customer ID"])
    
    # Convert date
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    # Remove negative values (returns)
    df = df[df["Quantity"] > 0]
    
    # Create total price
    df["TotalPrice"] = df["Quantity"] * df["Price"]
    
    # Use absolute path for the processed file
    processed_data_path = os.path.join(os.path.dirname(__file__), '../../data/processed/cleaned.csv')
    df.to_csv(processed_data_path, index=False)
    
    return df

if __name__ == "__main__":
    df = clean_data()
    print("Data cleaned successfully!")