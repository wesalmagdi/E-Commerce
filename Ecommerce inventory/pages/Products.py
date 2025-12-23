import streamlit as st
import pandas as pd
from utils import get_db_connection
from utils import check_low_stock_alerts

alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"{alert_count} Low Stock Alerts!")
    st.sidebar.info("Check the Dashboard or Inventory page for details.")
else:
    st.sidebar.success("Stock levels normal")

st.title("Product Management")

conn = get_db_connection()

df = pd.read_sql("SELECT * FROM product", conn)
st.dataframe(df, use_container_width=True)

st.divider()
st.subheader("Add New Product")
with st.form("add_product"):
    name = st.text_input("Product Name")
    sku = st.text_input("SKU (unique)")
    desc = st.text_area("Description")
    price = st.number_input("Price", min_value=0.0)
    vat = st.number_input("VAT Rate (%)", min_value=0.0, value=15.0) 
    
    if st.form_submit_button("Add to System"):
        cursor = conn.cursor()
        query = "INSERT INTO product (name, sku, description, price, vatrate) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, sku, desc, price, vat))
        conn.commit()
        st.success("Product successfully added!")
        st.rerun()

conn.close()