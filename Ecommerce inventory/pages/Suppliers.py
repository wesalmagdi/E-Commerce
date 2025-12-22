import streamlit as st
from utils import get_db_connection
import pandas as pd

st.title("Supplier Directory")

conn = get_db_connection()

with st.expander("Add New Supplier"):
    with st.form("supplier_form"):
        s_name = st.text_input("Supplier Company Name")
        contact = st.text_input("Contact Person")
        email = st.text_input("Email")
        if st.form_submit_button("Add Supplier"):
            cursor = conn.cursor()
            cursor.execute("INSERT INTO suppliers (name, contact_person, email) VALUES (%s, %s, %s)", (s_name, contact, email))
            conn.commit()
            st.success("Supplier Saved")

st.subheader("Current Suppliers")
df_s = pd.read_sql("SELECT * FROM suppliers", conn)
st.table(df_s)

conn.close()