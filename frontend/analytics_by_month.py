import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_summary/").json()
    df = (pd.DataFrame(response)
          .rename(columns={
              "expense_month": "Month Number",
              "month_name": "Month Name",
              "total": "Total"
          })
          .sort_values(by="Month Number", ascending=False)
          .set_index("Month Number"))

    st.title("Expense Breakdown By Months")
    st.bar_chart(df.set_index("Month Name")["Total"], use_container_width=True)
    st.table(df.assign(Total=df["Total"].map("{:.2f}".format)).sort_index())

