import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_db_connection, check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="IMS Dashboard", layout="wide")
apply_theme()

if st.sidebar.button(" Refresh Data"):
    st.rerun()

conn = get_db_connection()

df_alerts = pd.read_sql("SELECT * FROM lowstockalerts", conn)
alert_count = len(df_alerts)

if alert_count > 0:
    st.sidebar.error(f" {alert_count} Low Stock Alerts!")
else:
    st.sidebar.success("Stock levels normal")

st.title("Inventory Management System")
st.write("Live tracking of boutique stock and supplier orders.")

st.markdown("---")

if alert_count > 0:
    st.subheader("Urgent! Low Stock Alerts")
    st.dataframe(df_alerts, use_container_width=True)
else:
    st.success("All stock levels are currently healthy.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    df_stock = pd.read_sql("""
        SELECT p.name, i.stocklevel 
        FROM inventory i
        JOIN product p ON i.productid = p.productid
        ORDER BY i.stocklevel ASC
    """, conn)
    
    if not df_stock.empty:
        fig = px.bar(df_stock, x="name", y="stocklevel", 
                     title="Live Stock Levels",
                     labels={'name': 'Product Name', 'stocklevel': 'Quantity'},
                     color="stocklevel", 
                     color_continuous_scale="RdYlGn")
        
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No stock data available.")

with col2:
    df_orders = pd.read_sql("SELECT orderstatus, COUNT(*) as count FROM orders GROUP BY orderstatus", conn)
    
    if not df_orders.empty:
        fig2 = px.pie(df_orders, names="orderstatus", values="count", 
                      title="Order Status Distribution",
                      hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        
        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No order data available.")

conn.close()