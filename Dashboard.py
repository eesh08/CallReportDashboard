import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df

# ---------------------------------------------------------
# 2. PRODUCT LIST (P1–P4)
# ---------------------------------------------------------
def get_all_products(df):
    product_cols = ['P1','P2','P3','P4']
    products = pd.unique(df[product_cols].values.ravel('K'))
    products = pd.Series(products).dropna().unique()
    return sorted(products.tolist())

# ---------------------------------------------------------
# 3. FILTER FUNCTION (NO ROW DUPLICATION)
# ---------------------------------------------------------
def filter_by_product(df, product):
    if product == "All":
        return df
    return df[
        (df['P1'] == product) |
        (df['P2'] == product) |
        (df['P3'] == product) |
        (df['P4'] == product)
    ]

# ---------------------------------------------------------
# STREAMLIT UI SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Call Activity Dashboard", layout="wide")
st.title("📞 Call Activity Dashboard – 2025")

uploaded = st.file_uploader("Upload Call Data CSV", type=["csv"])

if not uploaded:
    st.info("Upload your CSV file to continue.")
    st.stop()

df = load_data(uploaded)

st.success("Data Loaded Successfully!")

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("FILTERS")

# Month filter
months = ["All"] + sorted(df["Month"].dropna().unique().tolist())
selected_month = st.sidebar.selectbox("Month", months)

# Employee filter
employees = ["All"] + sorted(df["In-Field Activity: Owner Name"].dropna().unique().tolist())
selected_emp = st.sidebar.selectbox("Employee / Owner", employees)

# Division filter
divisions = ["All"] + sorted(df["Division"].dropna().unique().tolist())
selected_div = st.sidebar.selectbox("Division", divisions)

# Territory filter
territories = ["All"] + sorted(df["Territory Code"].dropna().unique().tolist())
selected_terr = st.sidebar.selectbox("Territory", territories)

# Product filter
product_list = ["All"] + get_all_products(df)
selected_product = st.sidebar.selectbox("Product", product_list)

# ---------------------------------------------------------
# APPLY FILTERS (Order matters)
# ---------------------------------------------------------
filtered = df.copy()

if selected_month != "All":
    filtered = filtered[filtered["Month"] == selected_month]

if selected_emp != "All":
    filtered = filtered[filtered["In-Field Activity: Owner Name"] == selected_emp]

if selected_div != "All":
    filtered = filtered[filtered["Division"] == selected_div]

if selected_terr != "All":
    filtered = filtered[filtered["Territory Code"] == selected_terr]

filtered = filter_by_product(filtered, selected_product)

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.subheader("📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

total_calls = len(filtered)
unique_customers = filtered["Customer ID"].nunique()
unique_products = len(get_all_products(filtered))
clm_calls = filtered[filtered["Call with CLM"] == "YES"].shape[0]

c1.metric("Total Calls", f"{total_calls:,}")
c2.metric("Unique Customers Covered", f"{unique_customers:,}")
c3.metric("Products Discussed", f"{unique_products}")
c4.metric("CLM Calls", f"{clm_calls:,}")

# ---------------------------------------------------------
# CHART 1 – Calls Over Months
# ---------------------------------------------------------
if "Year Month" in filtered.columns:
    st.subheader("📅 Calls Trend Over Months")

    trend_df = (
        filtered.groupby("Year Month")
        .size()
        .reset_index(name="Total Calls")
        .sort_values("Year Month")
    )

    fig1 = px.line(trend_df, x="Year Month", y="Total Calls",
                   markers=True, title="Monthly Call Trend")
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------
# CHART 2 – Top Products
# ---------------------------------------------------------
st.subheader("💊 Top Products Discussed")

product_count = (
    filtered[['P1','P2','P3','P4']]
    .melt(value_name="Product")
    .dropna(subset=["Product"])
    .groupby("Product")
    .size()
    .reset_index(name="Count")
    .sort_values("Count", ascending=False)
)

fig2 = px.bar(product_count.head(10), 
              x="Product", y="Count", 
              title="Top 10 Discussed Products")
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------
# CHART 3 – Employee Productivity
# ---------------------------------------------------------
st.subheader("👤 Employee Productivity (Calls Made)")

emp_calls = (
    filtered.groupby("In-Field Activity: Owner Name")
    .size()
    .reset_index(name="Total Calls")
    .sort_values("Total Calls", ascending=False)
)

fig3 = px.bar(emp_calls.head(15),
              x="In-Field Activity: Owner Name", y="Total Calls",
              title="Top Performing Employees",
              labels={"In-Field Activity: Owner Name": "Employee"})
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# CHART 4 – Product vs Speciality Matrix
# ---------------------------------------------------------
st.subheader("🧪 Product × Speciality Analysis")

heat_df = (
    filtered[['Speciality','P1','P2','P3','P4']]
    .melt(id_vars='Speciality', value_name='Product')
    .dropna(subset=['Product'])
    .groupby(['Speciality','Product'])
    .size()
    .reset_index(name="Count")
)

fig4 = px.density_heatmap(
    heat_df,
    x="Product", y="Speciality", z="Count",
    color_continuous_scale="Blues",
    title="Product Discussion by Speciality"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------
# RAW DATA PREVIEW
# ---------------------------------------------------------
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered)
