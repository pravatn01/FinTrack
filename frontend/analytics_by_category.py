import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

def analytics_category_tab():
    start_date, end_date = st.columns(2)
    start_date = start_date.date_input("Start Date", datetime(2024, 1, 1))
    end_date = end_date.date_input("End Date", datetime(2024, 1, 31))

    if st.button("Get Analytics"):
        response = requests.post(
            f"{API_URL}/category_summary/",
            json={"start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")}
        ).json()

        df = pd.DataFrame(
            [(cat, round(data["percentage"], 2), data["total"]) for cat, data in response.items()],
            columns=["Category", "Percentage", "Total Expense (₹)"]
        ).sort_values(by="Percentage", ascending=False)

        st.title("Expense Breakdown By Category")
        fig = px.pie(
            df, names="Category", values="Percentage", hole=0.35,
            color_discrete_sequence=px.colors.sequential.Reds
        ).update_traces(
            textinfo="percent+label", textfont_size=14,
            pull=[0.06] + [0] * (len(df) - 1),
            hovertemplate="%{label}<br>Percentage: %{value:.2f}%"
        ).update_layout(showlegend=False, margin=dict(l=60, r=40, t=80, b=80), height=500, width=700)

        st.plotly_chart(fig, use_container_width=True)

        st.table(df.assign(
            **{
                "Total Expense (₹)": df["Total Expense (₹)"].map("{:,.2f}".format),
                "Percentage": df["Percentage"].map(lambda x: f"{x:.2f}%")
            }
        ))
