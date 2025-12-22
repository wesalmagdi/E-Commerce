import streamlit as st
from utils import get_db_connection
import pandas as pd

st.title("Record a Sale")

conn = get_db_connection()

df_p = pd.read_sql("SELECT product_id, name, price, stock_quantity FROM products", conn)
product_options = {row['name']: row['product_id'] for _, row in df_p.iterrows()}

with st.form("sale_form"):
    selected_name = st.selectbox("Select Product", options=list(product_options.keys()))
    quantity = st.number_input("Quantity Sold", min_value=1)
    
    if st.form_submit_button("Confirm Sale"):
        p_id = product_options[selected_name]
        current_stock = df_p[df_p['product_id'] == p_id]['stock_quantity'].values[0]
        unit_price = df_p[df_p['product_id'] == p_id]['price'].values[0]

        if current_stock >= quantity:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO orders (product_id, quantity, total_price) VALUES (%s, %s, %s)", 
                           (p_id, quantity, (unit_price * quantity)))
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s", 
                           (quantity, p_id))
            conn.commit()
            st.success(f"Sale recorded! Remaining stock: {current_stock - quantity}")
        else:
            st.error("Not enough stock available!")

conn.close()