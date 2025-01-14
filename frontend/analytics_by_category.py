import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_category_tab():
    start_date, end_date = st.columns(2)
    start_date = start_date.date_input("Start Date", datetime(2024, 8, 1))
    end_date = end_date.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/category_summary/", json=payload).json()

        df = pd.DataFrame({
            "Category": list(response.keys()),
            "Total": [response[cat]["total"] for cat in response],
            "Percentage": [response[cat]["percentage"] for cat in response]
        }).sort_values(by="Percentage", ascending=False)

        st.title("Expense Breakdown By Category")
        st.bar_chart(data=df.set_index("Category")["Percentage"], use_container_width=True)
        st.table(df.assign(
            Total=df["Total"].map("{:.2f}".format),
            Percentage=df["Percentage"].map("{:.2f}".format)
        ))

