import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_db_connection
from utils import check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="IMS Dashboard", layout="wide")
apply_theme()

def get_alert_count():
    conn = get_db_connection()
    df = pd.read_sql("select count(*) as count from lowstockalerts", conn)
    conn.close()
    return df['count'][0]

count = get_alert_count()
if count > 0:
    st.sidebar.error(f"{count} Low Stock Alerts!")
else:
    st.sidebar.success("Inventory Healthy")

st.title("Welcome to the E-commerce IMS")
st.write("Use the sidebar to navigate between Products, Inventory, and Orders.")




alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"{alert_count} Low Stock Alerts!")
    st.sidebar.info("Check the Dashboard or Inventory page for details.")
else:
    st.sidebar.success("Stock levels normal")
st.set_page_config(page_title="IMS Dashboard", layout="wide")
st.title("Inventory Dashboard")

conn = get_db_connection()

st.subheader("Urgent! Low Stock Alerts")
df_alerts = pd.read_sql("SELECT * FROM lowStockAlerts", conn)

if not df_alerts.empty:
    st.error(f"Action Required: {len(df_alerts)} items are below reorder points!")
    st.dataframe(df_alerts, use_container_width=True)
else:
    st.success("All stock levels are currently above reorder points.")

col1, col2 = st.columns(2)

with col1:
    df_stock = pd.read_sql("""
        SELECT p.name, i.stocklevel 
        FROM inventory i
        JOIN product p ON i.productid = p.productid
    """, conn)
    fig = px.bar(df_stock, x="name", y="stocklevel", title="Current Stock Levels")
    st.plotly_chart(fig)

with col2:
    df_orders = pd.read_sql("SELECT orderstatus, COUNT(*) as count FROM orders GROUP BY orderstatus", conn)
    fig2 = px.pie(df_orders, names="orderstatus", values="count", title="Order Status Distribution")
    st.plotly_chart(fig2)

conn.close()