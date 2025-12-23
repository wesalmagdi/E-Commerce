import streamlit as st 
import streamlit_authenticator as stauth
import yaml
import pandas as pd
from yaml.loader import SafeLoader
from utils import get_db_connection
from style_utils import apply_theme 

st.set_page_config(page_title=" IMS Home", page_icon="", layout="wide")
apply_theme()

try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Missing config.yaml! Please ensure it exists.")
    st.stop()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login(location='main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    
    username = st.session_state["username"]
    
    user_role = config['credentials']['usernames'][username]['roles'][0]
    
    st.session_state['user_role'] = user_role
    st.session_state['name'] = config['credentials']['usernames'][username]['name']

    conn = get_db_connection()
    if not conn:
        st.error("Database connection failed.")
        st.stop()

    if user_role == "admin":
        st.title(" Management System")
        st.markdown(f"#Welcome back, **{st.session_state['name']}**! ")
        st.write("Use the sidebar to navigate between Products, Inventory, and Orders.")
        
        st.markdown("---")
        st.subheader("Inventory")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            df_stock = pd.read_sql("SELECT SUM(stocklevel) as total FROM inventory", conn)
            raw_stock = df_stock['total'].iloc[0]
            val = int(raw_stock) if pd.notna(raw_stock) else 0
            st.metric("Total Items on Shelves", f"{val:,}")
            
        with col2:
            df_con = pd.read_sql("SELECT COUNT(*) as count FROM contract WHERE enddate >= CURDATE()", conn)
            st.metric("Active Contracts", df_con['count'].iloc[0] if not df_con.empty else 0)
            
        with col3:
            df_perf = pd.read_sql("SELECT COUNT(*) as count FROM supplierperformance WHERE shippingspeed = 'fast'", conn)
            st.metric("Top Performing Suppliers", df_perf['count'].iloc[0] if not df_perf.empty else 0)

        try:
            df_alerts = pd.read_sql("SELECT COUNT(*) as count FROM lowstockalerts", conn)
            alert_count = df_alerts['count'].iloc[0] if pd.notna(df_alerts['count'].iloc[0]) else 0
            if alert_count > 0:
                st.error(f"**Urgent! Low Stock Alerts:** There are {alert_count} items currently below reorder points.")
            else:
                st.success(" **Stock Status:** All  inventory levels are currently healthy.")
        except:
            pass

    else:
        st.title("Supplier Portal")
        st.markdown(f"# Welcome, **{st.session_state['name']}**")
        st.write("Your dashboard is filtered to show your specific performance and supply status.")
        
        st.markdown("---")
        
        supplier_alert_query = f"""
            SELECT COUNT(*) as count 
            FROM lowstockalerts l
            JOIN supplierperformance s ON l.productid = s.productid
            WHERE s.suppliername = '{st.session_state['name']}'
        """
        try:
            df_my_alerts = pd.read_sql(supplier_alert_query, conn)
            my_alert_count = df_my_alerts['count'].iloc[0] if pd.notna(df_my_alerts['count'].iloc[0]) else 0
            if my_alert_count > 0:
                st.warning(f" **Stock Alert:** {my_alert_count} of your items are running low in our warehouse.")
            else:
                st.success("Your supplied products are currently well-stocked.")
        except:
            pass

        query = f"SELECT COUNT(*) as count FROM supplierperformance WHERE suppliername = '{st.session_state['name']}'"
        df_my_perf = pd.read_sql(query, conn)
        st.metric("Your Tracked Products", df_my_perf['count'].iloc[0] if not df_my_perf.empty else 0)
        st.info("Navigate to the **Reports** tab for lead time analysis.")

    conn.close()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    
elif st.session_state["authentication_status"] is None:
    st.title("IMS")
    st.info("Please log in to manage inventory.")
    st.stop()