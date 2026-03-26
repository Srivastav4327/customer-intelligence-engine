import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/processed/rfm.csv")

features = df[["Recency", "Frequency", "Monetary"]]

scaler = StandardScaler()
scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(scaled)

print(df.groupby("cluster").mean())


def label_segment(row):
    if row["Monetary"] > 5000:
        return "High Value"
    elif row["Frequency"] > 5:
        return "Regular"
    else:
        return "At Risk"


df["segment"] = df.apply(label_segment, axis=1)
df.to_csv("data/processed/customer_segments.csv", index=False)
print("Segmentation saved!")
