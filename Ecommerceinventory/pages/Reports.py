import streamlit as st
import pandas as pd
from utils import get_db_connection
from style_utils import apply_girly_theme

st.set_page_config(page_title="Analytics Boutique", layout="wide")
apply_girly_theme()

st.title("Management Reports")

tab1, tab2, tab3 = st.tabs(["Stock Alerts", "Supplier Speed", "Valuation"])

conn = get_db_connection()

with tab1:
    st.subheader("Low Stock Emergency")
    df_low = pd.read_sql("select * from lowstockreport", conn)
    if not df_low.empty:
        st.dataframe(df_low.style.background_gradient(cmap='PuBu'), use_container_width=True)
    else:
        st.info("All shelves are beautifully stocked!")

with tab2:
    st.subheader("Supplier Shipping Speed")
    df_perf = pd.read_sql("select * from view_supplier_performance", conn)
    
    def color_speed(val):
        color = '#BDE0FE' if val == 'fast' else '#FFC2D1' if val == 'slow' else '#F8BBD0'
        return f'background-color: {color}'

    st.dataframe(df_perf.style.applymap(color_speed, subset=['shipping_speed']), use_container_width=True)

with tab3:
    st.subheader("Inventory Financial Value")
    df_val = pd.read_sql("select * from view_inventory_valuation", conn)
    total_value = df_val['total_inventory_value'].sum()
    st.metric("Total Boutique Value", f"${total_value:,.2f}")
    st.dataframe(df_val, use_container_width=True)

conn.close()