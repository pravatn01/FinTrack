import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px
import os

if "localhost" in os.getenv("HOST", "localhost"):
    API_URL = "http://localhost:8000"
else:
    API_URL = "https://fintrack-app.streamlit.app"

def analytics_category_tab():
    st.markdown("""
        <h2 style='font-family: "Poppins", sans-serif; font-size: 32px; color: #ff4b4b;'>Category Analytics</h2>
        <hr style='margin-top: 0; margin-bottom: 20px;'>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", datetime(2024, 1, 1))
    end_date = col2.date_input("End Date", datetime(2024, 1, 31))

    if st.button("Get Analytics"):
        try:
            response = requests.post(
                f"{API_URL}/category_summary/",
                json={
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
            )
            if response.status_code == 200:
                try:
                    response_data = response.json()
                except requests.exceptions.JSONDecodeError:
                    st.warning("The API returned an invalid JSON response.")
                    return
            else:
                st.warning(f"Failed to fetch data: {response.status_code} - {response.text}")
                return
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
            return

        try:
            df = pd.DataFrame(
                [(cat, round(data["percentage"], 2), data["total"]) for cat, data in response_data.items()],
                columns=["Category", "Percentage", "Total Expense (₹)"]
            ).sort_values(by="Percentage", ascending=False)
            df = df[["Category", "Total Expense (₹)", "Percentage"]]
        except (KeyError, TypeError, ValueError):
            st.error("Unexpected data format in the API response.")
            return

        st.markdown("<h3 style='font-size: 24px;'>Expense Distribution By Category</h3>", unsafe_allow_html=True)
        fig = px.pie(
            df,
            names="Category",
            values="Percentage",
            hole=0.35,
            color_discrete_sequence=px.colors.sequential.Reds
        ).update_traces(
            textinfo="percent+label",
            textfont_size=14,
            pull=[0.06] + [0] * (len(df) - 1),
            hovertemplate="%{label}<br>Percentage: %{value:.2f}%"
        ).update_layout(
            showlegend=False,
            margin=dict(l=60, r=40, t=80, b=80),
            height=500,
            width=700
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h3 style='font-size: 20px;'>Category Expense Summary</h3>", unsafe_allow_html=True)
        st.table(df.style.format({
            "Total Expense (₹)": "{:,.2f}",
            "Percentage": "{:.2f}%"
        }))
