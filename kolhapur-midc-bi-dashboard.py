import streamlit as st
import pandas as pd

st.set_page_config(page_title="MIDC BI Dashboard Demo", layout="wide")

st.title("📊 Kolhapur MIDC – Smart Factory Dashboard (Industry 4.0)")
st.markdown("Upload your factory Excel data and instantly visualize insights.")

# File upload
uploaded_file = st.file_uploader("Upload Factory Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Expecting columns: Date, Machine, Production, Downtime, Profit
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar filters
    st.sidebar.header("Filters")
    machines = st.sidebar.multiselect("Select Machine", df['Machine'].unique(), default=df['Machine'].unique())
    date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])

    filtered_df = df[(df['Machine'].isin(machines)) &
                     (df['Date'] >= pd.to_datetime(date_range[0])) &
                     (df['Date'] <= pd.to_datetime(date_range[1]))]

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Production", int(filtered_df['Production'].sum()))
    col2.metric("Avg Downtime", int(filtered_df['Downtime'].mean()))
    col3.metric("Avg Profit %", int(filtered_df['Profit'].mean()))

    # Charts
    st.subheader("Production Trend")
    st.line_chart(filtered_df.groupby('Date')['Production'].sum())

    st.subheader("Downtime by Machine")
    st.bar_chart(filtered_df.groupby('Machine')['Downtime'].mean())

    st.subheader("Profit Trend")
    st.line_chart(filtered_df.groupby('Date')['Profit'].mean())

    # Machine-level insights
    st.subheader("⚙️ Machine-Level Insights")
    worst_machine = filtered_df.groupby('Machine')['Downtime'].mean().idxmax()
    best_machine = filtered_df.groupby('Machine')['Production'].sum().idxmax()

    st.warning(f"Highest Downtime Machine: {worst_machine}")
    st.success(f"Best Performing Machine: {best_machine}")

    st.info("👉 Identify which machines need maintenance and which drive profits.")

else:
    st.info("Upload a sample Excel file with columns: Date, Machine, Production, Downtime, Profit")

st.markdown("---")
st.success("This is a real Industry 4.0 dashboard for MSMEs 🚀")
