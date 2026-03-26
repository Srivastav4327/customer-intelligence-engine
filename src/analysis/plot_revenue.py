import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/sql_outputs/revenue_data.csv")

plt.figure()
plt.plot(df["month"], df["revenue"])
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
plt.tight_layout()

plt.savefig("assets/revenue_trend.png")
print("Graph saved!")
