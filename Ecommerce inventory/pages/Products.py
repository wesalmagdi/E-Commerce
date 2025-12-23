import streamlit as st
from utils import get_db_connection
import pandas as pd

st.set_page_config(page_title="Product Management")
st.title("Product Management")

is_admin = "admin" in st.session_state.get("roles", [])

conn = get_db_connection()
df = pd.read_sql("SELECT * FROM products", conn)
st.dataframe(df, use_container_width=True)

if is_admin:
    st.divider()
    st.subheader("Add New Product")
    with st.form("add_product"):
        name = st.text_input("Name")
        cat = st.selectbox("Category", ["Electronics", "Home", "Clothing", "Food"])
        price = st.number_input("Price", min_value=0.0)
        qty = st.number_input("Initial Stock", min_value=0)
        
        if st.form_submit_button("Save Product"):
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)", 
                           (name, cat, price, qty))
            conn.commit()
            st.success("Product Added!")
            st.rerun()
conn.close()