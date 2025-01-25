import streamlit as st
from datetime import datetime
import requests
import os

if "localhost" in os.getenv("HOST", "localhost"):
    API_URL = "http://localhost:8000"
else:
    API_URL = "https://fintrack-app.streamlit.app"

def add_update_tab():
    selected_date = st.date_input(
        "Enter Date",
        datetime(2024, 8, 1),
        label_visibility="collapsed"
    )

    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        if response.status_code == 200:
            try:
                existing_expenses = response.json()
            except requests.exceptions.JSONDecodeError:
                st.warning("The response from the server is not in JSON format.")
                existing_expenses = []
        else:
            st.warning(f"Failed to fetch data: {response.status_code} - {response.text}")
            existing_expenses = []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
        existing_expenses = []

    categories = ["Entertainment", "Food", "Rent", "Shopping", "Others"]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("💵 **Amount**")
        with col2: st.markdown("📂 **Category**")
        with col3: st.markdown("📝 **Notes**")

        expenses = []
        for i in range(5):
            expense_data = existing_expenses[i] if i < len(existing_expenses) else {
                'amount': 0.0,
                'category': "Others",
                'notes': ""
            }
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=10.0,
                    value=expense_data['amount'],
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    "Category",
                    categories,
                    index=categories.index(expense_data['category']),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    "Notes",
                    value=expense_data['notes'],
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Update Expenses")
        if submit_button:
            with st.spinner("Updating expenses..."):
                filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
                try:
                    response = requests.post(
                        f"{API_URL}/expenses/{selected_date}",
                        json=filtered_expenses
                    )
                    if response.status_code == 200:
                        st.success("Expenses updated successfully!")
                    else:
                        st.error(f"Failed to update expenses: {response.status_code} - {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the API: {e}")
