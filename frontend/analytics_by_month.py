import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

def analytics_months_tab():
    df = pd.DataFrame(requests.get(f"{API_URL}/monthly_summary/").json()).rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month",
        "total": "Total Expense (₹)"
    }).sort_values(by="Month Number").set_index("Month Number")

    df['Total Expense (₹)'] = df['Total Expense (₹)'].map("{:,.2f}".format)
    st.title("Monthly Expense Trend")

    fig = px.line(df.reset_index(), x="Month", y="Total Expense (₹)", markers=True)
    fig.update_traces(line=dict(color="royalblue", width=3), marker=dict(size=7, color="red"))
    fig.update_layout(
        title_text="", plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=13, color="white")),
        yaxis=dict(showgrid=True, zeroline=False, tickfont=dict(size=13, color="white")),
        hovermode="x unified", margin=dict(l=60, r=40, t=40, b=80),
        xaxis_title_standoff=20, yaxis_title_standoff=20
    )
    st.plotly_chart(fig, use_container_width=True)
    st.table(df[['Month', 'Total Expense (₹)']])
