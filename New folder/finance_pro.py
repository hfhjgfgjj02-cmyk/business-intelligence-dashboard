import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Intelligence Dashboard", layout="wide")

st.title("📊 Business Intelligence Dashboard")

# Load Data
df = pd.read_csv("company_data.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month

# -------------------------
# SIDEBAR FILTERS
# -------------------------

st.sidebar.header("Dashboard Filters")

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

department = st.sidebar.multiselect(
    "Select Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

df = df[(df["Region"].isin(region)) & (df["Department"].isin(department))]

# -------------------------
# KPI METRICS
# -------------------------

revenue = df["Revenue"].sum()
expenses = df["Expenses"].sum()
profit = df["Profit"].sum()
units = df["Units_Sold"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"${revenue:,}")
c2.metric("💸 Total Expenses", f"${expenses:,}")
c3.metric("📈 Total Profit", f"${profit:,}")
c4.metric("📦 Units Sold", f"{units:,}")

st.divider()

# -------------------------
# REVENUE TREND
# -------------------------

st.subheader("📈 Revenue Trend")

trend = df.groupby("Date")["Revenue"].sum().reset_index()

fig1 = px.line(trend, x="Date", y="Revenue", markers=True)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# REGION PERFORMANCE
# -------------------------

st.subheader("🌍 Revenue by Region")

region_data = df.groupby("Region")["Revenue"].sum().reset_index()

fig2 = px.bar(region_data, x="Region", y="Revenue", color="Region")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# DEPARTMENT PERFORMANCE
# -------------------------

st.subheader("🏭 Department Performance")

dept_data = df.groupby("Department")["Profit"].sum().reset_index()

fig3 = px.pie(dept_data, names="Department", values="Profit", hole=0.4)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# EMPLOYEE PRODUCTIVITY
# -------------------------

st.subheader("👥 Employee Productivity")

prod = df.groupby("Department")[["Revenue","Employees"]].sum().reset_index()
prod["Revenue_per_Employee"] = prod["Revenue"] / prod["Employees"]

fig4 = px.bar(prod, x="Department", y="Revenue_per_Employee", color="Department")

st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# DATA TABLE
# -------------------------

st.subheader("📋 Company Data")

st.dataframe(df)