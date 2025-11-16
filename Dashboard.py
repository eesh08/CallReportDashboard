import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. LOAD DATA (Excel)
# ---------------------------------------------------------
@st.cache_data
def load_data(file):
    if file is None:
        return None

    # Read first sheet; auto-detect header row
    xls = pd.ExcelFile(file)
    sheet = xls.sheet_names[0]

    preview = pd.read_excel(xls, sheet_name=sheet, header=None, nrows=20)
    header_row = 0
    header_hints = ["owner", "in-field", "p1", "p2", "territory", "division", "customer", "month", "date"]
    for i in range(len(preview)):
        row_text = " ".join(preview.iloc[i].astype(str).str.lower().tolist())
        if any(h in row_text for h in header_hints):
            header_row = i
            break

    df = pd.read_excel(xls, sheet_name=sheet, header=header_row)
    df.columns = [str(c).strip() for c in df.columns]

    # Standardize common column names
    rename = {}
    for c in df.columns:
        lc = c.lower()
        if lc in {"p1", "product1", "product 1"}: rename[c] = "P1"
        elif lc in {"p2", "product2", "product 2"}: rename[c] = "P2"
        elif lc in {"p3", "product3", "product 3"}: rename[c] = "P3"
        elif lc in {"p4", "product4", "product 4"}: rename[c] = "P4"
        elif "owner name" in lc or lc.startswith("in-field"):
            rename[c] = "In-Field Activity: Owner Name"
        elif "territory" in lc and "code" in lc:
            rename[c] = "Territory Code"
        elif lc == "division":
            rename[c] = "Division"
        elif ("customer" in lc and "id" in lc) or lc == "customer id":
            rename[c] = "Customer ID"
        elif lc in {"year month", "year-month", "yr month"}:
            rename[c] = "Year Month"
        elif lc in {"month", "mnth"}:
            rename[c] = "Month"
        elif lc in {"date", "call date", "activity date"}:
            rename[c] = "Date"
        elif "clm" in lc:
            rename[c] = "Call with CLM"
    if rename:
        df = df.rename(columns=rename)

    # Derive Month / Year Month from Date if needed
    if "Date" in df.columns:
        dt = pd.to_datetime(df["Date"], errors="coerce")
        if "Month" not in df.columns:
            df["Month"] = dt.dt.strftime("%b")
        if "Year Month" not in df.columns:
            df["Year Month"] = dt.dt.to_period("M").astype(str)

    return df

# ---------------------------------------------------------
# 2. PRODUCT LIST (P1–P4)
# ---------------------------------------------------------
def get_all_products(df):
    product_cols = [c for c in ["P1", "P2", "P3", "P4"] if c in df.columns]
    if not product_cols:
        return []
    products = pd.unique(df[product_cols].values.ravel("K"))
    products = pd.Series(products).dropna().unique()
    return sorted(map(str, products.tolist()))

# ---------------------------------------------------------
# 3. FILTER FUNCTION (NO ROW DUPLICATION)
# ---------------------------------------------------------
def filter_by_product(df, product):
    if product == "All":
        return df
    product_cols = [c for c in ["P1", "P2", "P3", "P4"] if c in df.columns]
    if not product_cols:
        return df
    mask = df[product_cols].astype(str).eq(str(product)).any(axis=1)
    return df[mask]

# ---------------------------------------------------------
# STREAMLIT UI SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Call Activity Dashboard", layout="wide")
st.title("📞 Call Activity Dashboard – 2025")

# Excel-only uploader
uploaded = st.file_uploader("Upload Call Data Excel (.xlsx or .xls)", type=["xlsx", "xls"])

if not uploaded:
    st.info("Please upload an Excel file (.xlsx or .xls).")
    st.stop()

df = load_data(uploaded)
if df is None or df.empty:
    st.error("Could not read data from the uploaded Excel file.")
    st.stop()

st.success("Data Loaded Successfully!")

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("FILTERS")

months = ["All"] + sorted(df.get("Month", pd.Series(dtype=str)).dropna().astype(str).unique().tolist())
selected_month = st.sidebar.selectbox("Month", months)

employees = ["All"] + sorted(df.get("In-Field Activity: Owner Name", pd.Series(dtype=str)).dropna().astype(str).unique().tolist())
selected_emp = st.sidebar.selectbox("Employee / Owner", employees)

divisions = ["All"] + sorted(df.get("Division", pd.Series(dtype=str)).dropna().astype(str).unique().tolist())
selected_div = st.sidebar.selectbox("Division", divisions)

territories = ["All"] + sorted(df.get("Territory Code", pd.Series(dtype=str)).dropna().astype(str).unique().tolist())
selected_terr = st.sidebar.selectbox("Territory", territories)

product_list = ["All"] + get_all_products(df)
selected_product = st.sidebar.selectbox("Product", product_list)

# ---------------------------------------------------------
# APPLY FILTERS (Order matters)
# ---------------------------------------------------------
filtered = df.copy()

if selected_month != "All" and "Month" in filtered.columns:
    filtered = filtered[filtered["Month"].astype(str) == str(selected_month)]

if selected_emp != "All" and "In-Field Activity: Owner Name" in filtered.columns:
    filtered = filtered[filtered["In-Field Activity: Owner Name"].astype(str) == str(selected_emp)]

if selected_div != "All" and "Division" in filtered.columns:
    filtered = filtered[filtered["Division"].astype(str) == str(selected_div)]

if selected_terr != "All" and "Territory Code" in filtered.columns:
    filtered = filtered[filtered["Territory Code"].astype(str) == str(selected_terr)]

filtered = filter_by_product(filtered, selected_product)

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.subheader("📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

total_calls = len(filtered)
unique_customers = filtered.get("Customer ID", pd.Series(dtype=object)).nunique()
unique_products = len(get_all_products(filtered))
clm_calls = 0
if "Call with CLM" in filtered.columns:
    clm_calls = filtered[filtered["Call with CLM"].astype(str).str.upper() == "YES"].shape[0]

c1.metric("Total Calls", f"{total_calls:,}")
c2.metric("Unique Customers Covered", f"{unique_customers:,}")
c3.metric("Products Discussed", f"{unique_products}")
c4.metric("CLM Calls", f"{clm_calls:,}")

# ---------------------------------------------------------
# CHART 1 – Calls Over Months
# ---------------------------------------------------------
if "Year Month" in filtered.columns:
    tmp = (
        filtered.assign(_ym=pd.to_datetime(filtered["Year Month"], errors="coerce"))
        .dropna(subset=["_ym"])
        .groupby("_ym")
        .size()
        .reset_index(name="Calls")
        .sort_values("_ym")
    )
    fig1 = px.line(tmp, x="_ym", y="Calls", markers=True, title="Calls Over Time")
    fig1.update_layout(xaxis_title="Year-Month", yaxis_title="Calls")
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------
# CHART 2 – Top Products
# ---------------------------------------------------------
st.subheader("💊 Top Products Discussed")
product_cols = [c for c in ["P1", "P2", "P3", "P4"] if c in filtered.columns]
if product_cols:
    product_count = (
        filtered[product_cols]
        .melt(value_name="Product")
        .dropna(subset=["Product"])
        .groupby("Product")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    fig2 = px.bar(product_count.head(10), x="Product", y="Count", title="Top 10 Discussed Products")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No product columns (P1–P4) found.")

# ---------------------------------------------------------
# CHART 3 – Employee Productivity
# ---------------------------------------------------------
st.subheader("👤 Employee Productivity (Calls Made)")
if "In-Field Activity: Owner Name" in filtered.columns:
    emp_calls = (
        filtered.groupby("In-Field Activity: Owner Name")
        .size()
        .reset_index(name="Total Calls")
        .sort_values("Total Calls", ascending=False)
    )
    fig3 = px.bar(
        emp_calls.head(15),
        x="In-Field Activity: Owner Name",
        y="Total Calls",
        title="Top Performing Employees",
        labels={"In-Field Activity: Owner Name": "Employee"},
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# CHART 4 – Product vs Speciality Matrix
# ---------------------------------------------------------
st.subheader("🧪 Product × Speciality Analysis")
if "Speciality" in filtered.columns and product_cols:
    heat_df = (
        filtered[["Speciality"] + product_cols]
        .melt(id_vars="Speciality", value_name="Product")
        .dropna(subset=["Product"])
        .groupby(["Speciality", "Product"])
        .size()
        .reset_index(name="Count")
    )
    fig4 = px.density_heatmap(
        heat_df, x="Product", y="Speciality", z="Count",
        color_continuous_scale="Blues", title="Product Discussion by Speciality"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------------
# RAW DATA PREVIEW
# ---------------------------------------------------------
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered, use_container_width=True, height=420)
