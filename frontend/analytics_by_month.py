import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_data = response.json()
    df = pd.DataFrame(monthly_data).rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month",
        "total": "Total Expense (₹)"
    }).sort_values("Month Number").set_index("Month Number")

    st.markdown("""
        <h2 style='font-family: "Poppins", sans-serif; font-size: 32px; color: #ff4b4b;'>Monthly Analytics</h2>
        <hr style='margin-bottom: 20px;'>
        <h3 style='font-size: 24px;'>Monthly Expense Trends</h3>
    """, unsafe_allow_html=True)

    fig = px.line(
        df.reset_index(),
        x="Month",
        y="Total Expense (₹)",
        markers=True
    )
    fig.update_traces(
        line=dict(color="#fff5f0", width=3),
        marker=dict(size=10, color="#fb6a4a")
    )
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=13, color="white")),
        yaxis=dict(showgrid=True, zeroline=False, tickfont=dict(size=13, color="white")),
        hovermode="x unified",
        margin=dict(l=60, r=40, t=40, b=80)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<h3 style='font-size: 20px;'>Monthly Expense Summary</h3>", unsafe_allow_html=True)
    st.table(df.style.format({
    "Total Expense (₹)": "{:,.2f}".format
    }))
