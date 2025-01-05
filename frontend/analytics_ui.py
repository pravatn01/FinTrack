import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date', datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input('End Date', datetime(2024, 8, 5))
