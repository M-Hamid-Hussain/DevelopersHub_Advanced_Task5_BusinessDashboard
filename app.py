import pandas as pd
import streamlit as st
import plotly.express as px

# Page Config
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>📊 Superstore Business Dashboard</h1>", unsafe_allow_html=True)

# Load Data
df = pd.read_excel("global_superstore_2016.xlsx")

# Sidebar Filters
st.sidebar.header("🔎 Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

# Apply Filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]

# ================= KPIs =================
st.markdown("## 📊 Key Performance Indicators")

# Calculate KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

# Format values (in Millions for clean display)
sales_display = f"${total_sales/1_000_000:.2f}M"
profit_display = f"${total_profit/1_000_000:.2f}M"
orders_display = f"{total_orders:,}"

# Create columns
col1, col2, col3 = st.columns(3)

# Display KPIs
col1.metric("💰 Total Sales", sales_display)
col2.metric("📈 Total Profit", profit_display)
col3.metric("📦 Total Orders", orders_display)

# ================= CHARTS =================
st.markdown("## 📊 Data Visualizations")

col4, col5 = st.columns(2)

# Sales by Category
sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig1 = px.bar(
    sales_by_category,
    x="Category",
    y="Sales",
    title="Sales by Category",
    color="Category"
)

col4.plotly_chart(fig1, use_container_width=True)

# Profit by Region
profit_by_region = filtered_df.groupby("Region")["Profit"].sum().reset_index()

fig2 = px.bar(
    profit_by_region,
    x="Region",
    y="Profit",
    title="Profit by Region",
    color="Region"
)

col5.plotly_chart(fig2, use_container_width=True)

# ================= TOP CUSTOMERS =================
st.markdown("## 🏆 Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

st.dataframe(top_customers, use_container_width=True)