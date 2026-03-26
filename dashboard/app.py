from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    h1, h2, h3 {
        letter-spacing: -0.02em;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(180deg, #fffaf2 0%, #fff 100%);
        border: 1px solid rgba(185, 122, 87, 0.18);
        border-radius: 16px;
        padding: 0.75rem;
        color: #1f2937;
    }
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #4b5563 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SEGMENT_COLORS = ["#c26d3a", "#4f7c82", "#d0a73f"]


@st.cache_data
def load_data():
    repo_root = Path(__file__).resolve().parents[1]
    segments_path = repo_root / "data" / "processed" / "customer_segments.csv"
    predictions_path = repo_root / "data" / "processed" / "churn_predictions.csv"

    segments = pd.read_csv(segments_path)

    if predictions_path.exists():
        predictions = pd.read_csv(predictions_path)
        prediction_cols = ["Customer ID", "prediction", "prediction_probability"]
        available_cols = [col for col in prediction_cols if col in predictions.columns]
        if available_cols:
            segments = segments.merge(
                predictions[available_cols].drop_duplicates(subset=["Customer ID"]),
                on="Customer ID",
                how="left",
            )

    return segments


df = load_data()

st.title("Customer Intelligence Dashboard")
st.caption("Customer segmentation, churn risk, and value trends in one view.")

st.sidebar.header("Filters")

segment_options = sorted(df["segment"].dropna().unique().tolist())
selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    options=segment_options,
    default=segment_options,
)

cluster_options = sorted(df["cluster"].dropna().astype(int).unique().tolist())
selected_clusters = st.sidebar.multiselect(
    "Cluster",
    options=cluster_options,
    default=cluster_options,
)

monetary_min = float(df["Monetary"].min())
monetary_max = float(df["Monetary"].max())
selected_monetary = st.sidebar.slider(
    "Monetary Range",
    min_value=float(monetary_min),
    max_value=float(monetary_max),
    value=(float(monetary_min), float(monetary_max)),
)

filtered = df[
    df["segment"].isin(selected_segments)
    & df["cluster"].astype(int).isin(selected_clusters)
    & df["Monetary"].between(selected_monetary[0], selected_monetary[1])
].copy()

if filtered.empty:
    st.warning("No customers match the current filter selection.")
    st.stop()

avg_churn_risk = (
    round(filtered["prediction_probability"].mean() * 100, 2)
    if "prediction_probability" in filtered.columns
    else None
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Customers", f"{len(filtered):,}")
kpi2.metric("Avg Revenue", f"${filtered['Monetary'].mean():,.2f}")
kpi3.metric("Avg Frequency", f"{filtered['Frequency'].mean():.2f}")
if avg_churn_risk is not None:
    kpi4.metric("Avg Churn Risk", f"{avg_churn_risk:.2f}%")
else:
    kpi4.metric("High Value Customers", f"{(filtered['segment'] == 'High Value').sum():,}")

segment_counts = (
    filtered["segment"]
    .value_counts()
    .rename_axis("segment")
    .reset_index(name="customers")
)

cluster_summary = (
    filtered.groupby("cluster", as_index=False)
    .agg(
        customers=("Customer ID", "count"),
        avg_recency=("Recency", "mean"),
        avg_frequency=("Frequency", "mean"),
        avg_monetary=("Monetary", "mean"),
    )
)

left_col, right_col = st.columns((1, 1))

with left_col:
    st.subheader("Segment Mix")
    segment_chart = (
        alt.Chart(segment_counts)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusBottomLeft=8)
        .encode(
            x=alt.X("customers:Q", title="Customers"),
            y=alt.Y("segment:N", sort="-x", title=None),
            color=alt.Color(
                "segment:N",
                scale=alt.Scale(range=SEGMENT_COLORS),
                legend=None,
            ),
            tooltip=["segment:N", "customers:Q"],
        )
        .properties(height=320)
    )
    st.altair_chart(segment_chart, use_container_width=True)

with right_col:
    st.subheader("Cluster Profile")
    cluster_chart = (
        alt.Chart(cluster_summary)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("cluster:O", title="Cluster"),
            y=alt.Y("avg_monetary:Q", title="Avg Monetary"),
            color=alt.Color(
                "cluster:O",
                scale=alt.Scale(range=["#4f7c82", "#c26d3a", "#d0a73f"]),
                legend=None,
            ),
            tooltip=[
                "cluster:O",
                "customers:Q",
                alt.Tooltip("avg_recency:Q", format=".2f"),
                alt.Tooltip("avg_frequency:Q", format=".2f"),
                alt.Tooltip("avg_monetary:Q", format=".2f"),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(cluster_chart, use_container_width=True)

st.subheader("Customer Value Map")
plot_data = filtered.sample(min(len(filtered), 1500), random_state=42)
value_map = (
    alt.Chart(plot_data)
    .mark_circle(opacity=0.75)
    .encode(
        x=alt.X("Frequency:Q", title="Frequency"),
        y=alt.Y("Monetary:Q", title="Monetary"),
        size=alt.Size("avg_order_value:Q", title="Avg Order Value", scale=alt.Scale(range=[40, 700])),
        color=alt.Color(
            "segment:N",
            scale=alt.Scale(range=SEGMENT_COLORS),
            legend=alt.Legend(title="Segment"),
        ),
        tooltip=[
            alt.Tooltip("Customer ID:Q", format=".0f"),
            alt.Tooltip("Recency:Q", format=".0f"),
            alt.Tooltip("Frequency:Q", format=".0f"),
            alt.Tooltip("Monetary:Q", format=".2f"),
            alt.Tooltip("avg_order_value:Q", format=".2f"),
            "segment:N",
            "cluster:O",
        ],
    )
    .properties(height=380)
)
st.altair_chart(value_map, use_container_width=True)

bottom_left, bottom_right = st.columns((1, 1))

with bottom_left:
    st.subheader("Revenue Distribution")
    revenue_hist = (
        alt.Chart(filtered)
        .mark_bar(color="#c26d3a")
        .encode(
            x=alt.X("Monetary:Q", bin=alt.Bin(maxbins=30), title="Monetary"),
            y=alt.Y("count():Q", title="Customers"),
            tooltip=["count():Q"],
        )
        .properties(height=300)
    )
    st.altair_chart(revenue_hist, use_container_width=True)

with bottom_right:
    st.subheader("Highest Churn Risk")
    if "prediction_probability" in filtered.columns:
        risk_table = (
            filtered.sort_values("prediction_probability", ascending=False)
            .loc[:, ["Customer ID", "segment", "cluster", "Monetary", "prediction_probability"]]
            .head(10)
            .rename(columns={"prediction_probability": "churn_risk"})
        )
        risk_chart = (
            alt.Chart(risk_table)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusBottomLeft=8)
            .encode(
                x=alt.X("churn_risk:Q", title="Predicted Churn Probability"),
                y=alt.Y("Customer ID:N", sort="-x", title="Customer ID"),
                color=alt.Color(
                    "segment:N",
                    scale=alt.Scale(range=SEGMENT_COLORS),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip("Customer ID:N"),
                    "segment:N",
                    "cluster:O",
                    alt.Tooltip("Monetary:Q", format=".2f"),
                    alt.Tooltip("churn_risk:Q", format=".3f"),
                ],
            )
            .properties(height=300)
        )
        st.altair_chart(risk_chart, use_container_width=True)
    else:
        st.info("Churn prediction data is not available yet.")

st.subheader("Customer Detail")
display_cols = [
    "Customer ID",
    "segment",
    "cluster",
    "Recency",
    "Frequency",
    "Monetary",
    "avg_order_value",
    "customer_lifespan",
]
if "prediction_probability" in filtered.columns:
    display_cols.append("prediction_probability")

st.dataframe(
    filtered[display_cols].sort_values("Monetary", ascending=False),
    use_container_width=True,
    hide_index=True,
)
