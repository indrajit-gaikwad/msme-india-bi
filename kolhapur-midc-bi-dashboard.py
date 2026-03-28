import streamlit as st
import pandas as pd

st.set_page_config(page_title="MIDC BI Dashboard Demo", layout="wide")

st.title("📊 Kolhapur MIDC – Smart Factory Dashboard (Industry 4.0)")
st.markdown("Upload your factory Excel data and instantly visualize insights.")

# File upload
uploaded_file = st.file_uploader("Upload File", type=["xlsx", "xls", "csv"])

if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
if uploaded_file:
    # df = pd.read_excel(uploaded_file)

    # Expected columns:
    # Date, Machine, Shift, Production, Downtime, Defects, Profit, Customer, Order_Value, Payment_Status

    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar filters
    st.sidebar.header("Filters")
    machines = st.sidebar.multiselect("Select Machine", df['Machine'].unique(), default=df['Machine'].unique())
    shifts = st.sidebar.multiselect("Select Shift", df['Shift'].unique(), default=df['Shift'].unique())
    customers = st.sidebar.multiselect("Select Customer", df['Customer'].unique(), default=df['Customer'].unique())

    date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])

    filtered_df = df[
        (df['Machine'].isin(machines)) &
        (df['Shift'].isin(shifts)) &
        (df['Customer'].isin(customers)) &
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1]))
    ]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Production", int(filtered_df['Production'].sum()))
    col2.metric("Avg Downtime", round(filtered_df['Downtime'].mean(), 1))
    col3.metric("Total Defects", int(filtered_df['Defects'].sum()))
    col4.metric("Avg Profit %", round(filtered_df['Profit'].mean(), 1))

    # Production Trend
    st.subheader("📈 Production Trend")
    prod_trend = filtered_df.groupby('Date')['Production'].sum()
    st.line_chart(prod_trend)

    # Downtime by Machine
    st.subheader("⚙️ Downtime by Machine")
    downtime_machine = filtered_df.groupby('Machine')['Downtime'].mean()
    st.bar_chart(downtime_machine)

    # Defects by Shift
    st.subheader("❌ Defects by Shift")
    defects_shift = filtered_df.groupby('Shift')['Defects'].sum()
    st.bar_chart(defects_shift)

    # Profit Trend
    st.subheader("💰 Profit Trend")
    profit_trend = filtered_df.groupby('Date')['Profit'].mean()
    st.line_chart(profit_trend)

    # Payment Status
    st.subheader("💳 Payment Status Overview")
    payment_status = filtered_df.groupby('Payment_Status')['Order_Value'].sum()
    st.bar_chart(payment_status)

    # Machine-level insights
    st.subheader("⚙️ Machine-Level Insights")
    worst_machine = filtered_df.groupby('Machine')['Downtime'].mean().idxmax()
    best_machine = filtered_df.groupby('Machine')['Production'].sum().idxmax()

    st.warning(f"Highest Downtime Machine: {worst_machine}")
    st.success(f"Best Performing Machine: {best_machine}")

    # Business insights
    st.subheader("📊 Business Insights")
    delayed_payments = filtered_df[filtered_df['Payment_Status'].isin(['Pending', 'Delayed'])]['Order_Value'].sum()
    st.error(f"Total Cash Stuck (Pending/Delayed): ₹{int(delayed_payments)}")

    st.info("👉 Identify production issues, machine problems, quality defects, and cash flow gaps instantly.")

else:
    st.info("Upload an Excel file with columns: Date, Machine, Shift, Production, Downtime, Defects, Profit, Customer, Order_Value, Payment_Status")

st.markdown("---")
st.success("This is a real Industry 4.0 dashboard for MSMEs 🚀")
