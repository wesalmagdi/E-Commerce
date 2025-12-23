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

st.title("Inventory & Sales Reports")

conn = get_db_connection()

tab1, tab2, tab3 = st.tabs(["Low Stock Log", "Supplier Performance", "Transaction Ledger"])

with tab1:
    st.subheader("Current Low Stock Alerts")
    df_low = pd.read_sql("SELECT * FROM lowstockalerts", conn)
    st.dataframe(df_low, use_container_width=True)
    
    csv = df_low.to_csv(index=False).encode('utf-8')
    st.download_button("Export Low Stock Report", data=csv, file_name="low_stock.csv", mime="text/csv")

with tab2:
    st.subheader("Supplier Summary")
    df_supp = pd.read_sql("SELECT name, email, minordervalue, currency FROM supplier", conn)
    st.table(df_supp)

with tab3:
    st.subheader("Order History")
    query = """
        SELECT o.orderid, s.name as supplier, o.orderstatus, o.ordereddate, o.receiveddate 
        FROM orders o
        JOIN supplier s ON o.supplierid = s.supplierid
    """
    df_orders = pd.read_sql(query, conn)
    st.dataframe(df_orders, use_container_width=True)

conn.close()