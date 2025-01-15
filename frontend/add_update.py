import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def fetch_expenses(selected_date):
    """Fetch expenses with a loading spinner"""
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    return response.json() if response.status_code == 200 else []

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 2, 1), label_visibility="collapsed")

    if "expenses" not in st.session_state or st.session_state.get("last_fetched_date") != selected_date:
        with st.spinner('Loading expenses...'):
            st.session_state.expenses = fetch_expenses(selected_date) + [{"amount": 0.0, "category": "Others", "notes": ""}]
            st.session_state.last_fetched_date = selected_date

    categories = ["Entertainment", "Food", "Rent", "Shopping", "Others"]

    with st.form(key="expense_form", clear_on_submit=True):
        for i, expense in enumerate(st.session_state.expenses):
            col1, col2, col3 = st.columns(3)
            with col1:
                expense['amount'] = st.number_input("", 0.0, 10000.0, expense['amount'], 10.0, key=f"amount_{i}", label_visibility="collapsed")
            with col2:
                expense['category'] = st.selectbox("", categories, categories.index(expense['category']), key=f"category_{i}", label_visibility="collapsed")
            with col3:
                expense['notes'] = st.text_input("", expense['notes'], key=f"notes_{i}", label_visibility="collapsed")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=[e for e in st.session_state.expenses if e['amount'] > 0])
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")
