
import duckdb
import pandas as pd
import streamlit as st
from datetime import datetime
from config import get_duckdb_path

st.set_page_config(page_title="E-commerce Revenue Dashboard", layout="wide")
st.title("E-commerce Revenue Dashboard")
st.caption("Reads DuckDB from the pipeline and shows daily metrics.")

# Connect
db_path = get_duckdb_path()
try:
    con = duckdb.connect(db_path, read_only=True)
except Exception as e:
    st.error(f"Could not open DuckDB at: {db_path}. Error: {e}")
    st.stop()

# Check table
try:
    available = set(con.execute("show tables").df()["name"].str.lower().tolist())
except Exception as e:
    st.error(f"Could not enumerate tables. Error: {e}")
    st.stop()

if "mart_revenue_daily" not in available:
    st.warning("Table 'mart_revenue_daily' not found. Run the data pipeline first.")
    st.stop()

# Load
df = con.execute("select * from mart_revenue_daily order by revenue_date").df()
con.close()
df["revenue_date"] = pd.to_datetime(df["revenue_date"])

# Filters
st.sidebar.header("Filters")
min_date = df["revenue_date"].min().date()
max_date = df["revenue_date"].max().date()
start, end = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(start, tuple):
    start, end = start
mask = (df["revenue_date"] >= pd.to_datetime(start)) & (df["revenue_date"] <= pd.to_datetime(end))
df_f = df.loc[mask].copy()

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Gross", f"${df_f['revenue_gross'].sum():,.0f}")
c2.metric("Paid", f"${df_f['revenue_paid'].sum():,.0f}")
c3.metric("Refunded", f"${df_f['revenue_refunded'].sum():,.0f}")
c4.metric("Failed", f"${df_f['revenue_failed'].sum():,.0f}")

st.divider()

# Chart
import matplotlib.pyplot as plt
st.subheader("Revenue by day")
fig = plt.figure()
plt.plot(df_f["revenue_date"], df_f["revenue_paid"], label="Paid")
plt.plot(df_f["revenue_date"], df_f["revenue_refunded"], label="Refunded")
plt.plot(df_f["revenue_date"], df_f["revenue_failed"], label="Failed")
plt.plot(df_f["revenue_date"], df_f["revenue_gross"], label="Gross")
plt.legend(); plt.xlabel("Date"); plt.ylabel("Amount"); plt.tight_layout()
st.pyplot(fig)

# Table
st.subheader("Daily table")
st.dataframe(df_f.sort_values("revenue_date", ascending=False), use_container_width=True)

st.info("Tip: set DUCKDB_PATH env var if your file is not at the default path.")
