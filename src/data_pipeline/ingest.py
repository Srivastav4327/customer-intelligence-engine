import pandas as pd

def load_data():
    file_path = "data/raw/online_retail_II.xlsx"
    
    df1 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
    df2 = pd.read_excel(file_path, sheet_name="Year 2010-2011")
    
    df = pd.concat([df1, df2])
    
    return df

if __name__ == "__main__":
    df = load_data()
    df.to_csv("data/raw/combined.csv", index=False)
    print("Data combined successfully!")
