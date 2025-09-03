import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import altair as alt
from databricks import sql

# ---------------------------
# 1. Databricks Connection
# ---------------------------
# Replace with your credentials or set them in Streamlit secrets
DATABRICKS_SERVER = st.secrets["databricks"]["server_hostname"]
DATABRICKS_HTTP_PATH = st.secrets["databricks"]["http_path"]
DATABRICKS_TOKEN = st.secrets["databricks"]["token"]

def query_databricks(sql_query):
    with sql.connect(
        server_hostname=DATABRICKS_SERVER,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)
        
# ---------------------------
# 2. App Header & Filters
# ---------------------------
st.set_page_config(page_title="E-commerce Analytics Dashboard", layout="wide")
st.title("E-commerce Analytics Dashboard")

# Example: Device filter
device_filter = st.multiselect(
    "Select Device Type(s):",
    ["Desktop", "Mobile", "Tablet"],
    default=["Desktop", "Mobile", "Tablet"]
)

# ---------------------------
# 3. Key Metrics (Cart Abandonment & Revenue)
# ---------------------------
st.header("Key Metrics")

# SQL queries (replace with your actual table names)
cart_query = "SELECT cart_abandonment_rate FROM cart_abandonment LIMIT 1"
revenue_query = "SELECT total_revenue, average_order_value FROM Revenue LIMIT 1"

cart_df = query_databricks(cart_query)
revenue_df = query_databricks(revenue_query)

cart_abandonment_rate = cart_df["cart_abandonment_rate"].iloc[0]
total_revenue = revenue_df["total_revenue"].iloc[0]
average_order_value = revenue_df["average_order_value"].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Cart Abandonment Rate", f"{cart_abandonment_rate*100:.1f}%")
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Average Order Value", f"${average_order_value:.2f}")

# ---------------------------
# 4. Device Type Performance
# ---------------------------
st.header("Device Type Performance")

device_query = """
SELECT device_type, purchases, sessions, conversion_rate
FROM device_types
"""
device_df = query_databricks(device_query)
filtered_df = device_df[device_df["device_type"].isin(device_filter)]

device_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="device_type",
    y="purchases",
    color="device_type",
    tooltip=["sessions", "purchases", "conversion_rate"]
).properties(width=500)

st.altair_chart(device_chart, use_container_width=True)

# ---------------------------
# 5. Funnel Analysis
# ---------------------------
st.header("Funnel Analysis")

# Fetch data
funnel_query = """
SELECT website_visits, product_views, add_to_cart, purchases, conversion_rate, drop_off_rate
FROM funnel_analysis
LIMIT 1
"""
funnel_df = query_databricks(funnel_query).T.reset_index()
funnel_df.columns = ["stage", "value"]

# Convert all values to numeric (in case they are strings)
funnel_df["value"] = pd.to_numeric(funnel_df["value"], errors="coerce")

# Define stages
funnel_stages = ["website_visits", "product_views", "add_to_cart", "purchases"]
metrics = ["conversion_rate", "drop_off_rate"]

funnel_data = funnel_df[funnel_df["stage"].isin(funnel_stages)]
metrics_data = funnel_df[funnel_df["stage"].isin(metrics)]

# Convert conversion_rate and drop_off_rate to percentages
metrics_data.loc[
    metrics_data["stage"].isin(["conversion_rate", "drop_off_rate"]), "value"
] = (
    metrics_data.loc[
        metrics_data["stage"].isin(["conversion_rate", "drop_off_rate"]), "value"
    ].astype(float) * 100
)

# Color mapping for funnel
funnel_colors = alt.Scale(
    domain=funnel_stages,
    range=["#4c78a8", "#72b7b2", "#a1c181", "#2ca02c"]  # purchases in green
)

# Funnel chart
funnel_chart = alt.Chart(funnel_data).mark_bar(size=40).encode(
    y=alt.Y("stage", sort=funnel_stages[::-1], axis=alt.Axis(title=None)),
    x="value",
    color=alt.Color("stage", scale=funnel_colors),
    tooltip=["stage", "value"]
).properties(
    width=600,
    title="Funnel Stages"
)

# Color mapping for metrics
metrics_colors = alt.Scale(
    domain=["conversion_rate", "drop_off_rate"],
    range=["#2ca02c", "#d62728"]  # green for conversion_rate, red for drop_off_rate
)

# Metrics chart
metrics_chart = alt.Chart(metrics_data).mark_bar().encode(
    x=alt.X("stage", sort=metrics),
    y=alt.Y(
        "value",
        axis=alt.Axis(format=".0f", title="Value (%)")  # show numbers as is, add (%) to label
    ),
    color=alt.Color("stage", scale=metrics_colors),
    tooltip=[
        alt.Tooltip("stage"),
        alt.Tooltip("value", format=".4f")  # show decimals for rates
    ]
).properties(
    width=600,
    title="Conversion Metrics"
)

st.altair_chart(funnel_chart, use_container_width=True)
st.altair_chart(metrics_chart, use_container_width=True)
# ---------------------------
# 6. Exit & Session Insights
# ---------------------------
st.header("Exit & Session Insights")

exit_query = """
SELECT purchase, avg_bounce_rates, avg_exit_rates
FROM exit_rates
"""
exit_df = query_databricks(exit_query)

exit_chart = alt.Chart(exit_df).mark_circle(size=200).encode(
    x="avg_bounce_rates",
    y="avg_exit_rates",
    color="purchase",
    tooltip=["avg_bounce_rates", "avg_exit_rates"]
)

st.altair_chart(exit_chart, use_container_width=True)