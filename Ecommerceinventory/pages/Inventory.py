import streamlit as st
from utils import get_db_connection
import pandas as pd

st.title("Inventory Tracking")

conn = get_db_connection()
df = pd.read_sql("SELECT name, stock_quantity, category FROM products", conn)

low_stock_threshold = 10
low_stock_count = len(df[df['stock_quantity'] < low_stock_threshold])

col1, col2 = st.columns(2)
col1.metric("Total Items", len(df))
col2.metric("Low Stock Items", low_stock_count, delta=-low_stock_count, delta_color="inverse")

st.subheader("Stock Levels")
st.dataframe(df.style.highlight_between(left=0, right=low_stock_threshold, subset=['stock_quantity'], color='#ff4b4b'))

conn.close()