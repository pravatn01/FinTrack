import streamlit as st
from add_update import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_month import analytics_months_tab

st.markdown("""
    <h1 style='font-family: "Poppins", sans-serif; font-size: 40px;'>
        <span style='color: #ff4b4b;'>Fin</span><span style='color: white;'>Track</span>
    </h1>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(
    ["📅 Add/Update Expenses", "📊 Category Analytics", "📈 Monthly Analytics"]
)

with tab1:
    add_update_tab()

with tab2:
    analytics_category_tab()

with tab3:
    analytics_months_tab()
