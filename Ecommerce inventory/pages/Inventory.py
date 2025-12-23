import streamlit as st
import pandas as pd
from utils import get_db_connection
from utils import check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="Inventory Chic", layout="wide")
apply_theme()
alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"{alert_count} Low Stock Alerts!")
    st.sidebar.info("Check the Dashboard or Inventory page for details.")
else:
    st.sidebar.success("Stock levels normal")

st.title("Stock Tracking")

conn = get_db_connection()

query = """
    SELECT p.name, i.location, i.stocklevel, i.reorderpoint 
    FROM inventory i
    JOIN product p ON i.productid = p.productid
"""
df_inv = pd.read_sql(query, conn)

low_stock = df_inv[df_inv['stocklevel'] <= df_inv['reorderpoint']]
st.metric("Total Stocked Items", len(df_inv))

if not low_stock.empty:
    st.warning(f"{len(low_stock)} items are at or below reorder points!")
    st.dataframe(low_stock, use_container_width=True)
else:
    st.success("All stock levels are healthy.")

st.subheader("Full Inventory List")
st.table(df_inv)

conn.close()