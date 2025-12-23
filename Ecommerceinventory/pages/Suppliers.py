import streamlit as st
import pandas as pd
from utils import get_db_connection
from utils import check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="Supplier Management", layout="wide")
apply_theme()

alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"{alert_count} Low Stock Alerts!")
    st.sidebar.info("Check the Dashboard or Inventory page for details.")
else:
    st.sidebar.success("Stock levels normal")

st.title("Supplier Management")

conn = get_db_connection()

with st.expander("Register New Supplier"):
    with st.form("supp_form"):
        name = st.text_input("Company Name")
        email = st.text_input("Email")
        val = st.number_input("Minimum Order Value", min_value=0.0)
        curr = st.selectbox("Currency", ["EGP", "USD", "EUR"])
        
        if st.form_submit_button("Register"):
            cursor = conn.cursor()
            query = "INSERT INTO supplier (name, email, minordervalue, currency) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, val, curr))
            conn.commit()
            st.rerun()

df_s = pd.read_sql("SELECT name, email, minordervalue, currency FROM supplier", conn)
st.dataframe(df_s, use_container_width=True)

conn.close()