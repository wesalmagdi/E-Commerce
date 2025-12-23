import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_db_connection
from utils import check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="Order Boutique", layout="wide")
apply_theme()
alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"{alert_count} Low Stock Alerts!")
    st.sidebar.info("Check the Dashboard or Inventory page for details.")
else:
    st.sidebar.success("Stock levels normal")

st.title("Receive Deliveries")

conn = get_db_connection()

query_pending = """
    SELECT o.orderid, s.name as supplier
    FROM orders o
    JOIN supplier s ON o.supplierid = s.supplierid
    WHERE o.orderstatus = 'pending'
"""
df_pending = pd.read_sql(query_pending, conn)

if not df_pending.empty:
    selected_order = st.selectbox("Select Pending Order ID", df_pending['orderid'])
    
    if st.button("Mark as Received & Update Stock"):
        cursor = conn.cursor()
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("UPDATE orders SET orderstatus = 'received', receiveddate = %s WHERE orderid = %s", (today, selected_order))
            
            update_stock_query = """
                UPDATE inventory i
                JOIN orderitem oi ON i.productid = oi.productid
                SET i.stocklevel = i.stocklevel + oi.quantity
                WHERE oi.orderid = %s
            """
            cursor.execute(update_stock_query, (selected_order,))
            
            conn.commit()
            st.success(f"Order #{selected_order} received. Inventory stock levels have been increased!")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating stock: {e}")
        finally:
            cursor.close()
else:
    st.info("No pending orders found.")

conn.close()