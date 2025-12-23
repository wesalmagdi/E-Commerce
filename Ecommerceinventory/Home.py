import streamlit as st 
import streamlit_authenticator as stauth
import yaml
import pandas as pd
from yaml.loader import SafeLoader
from utils import get_db_connection
from style_utils import apply_theme 

st.set_page_config(page_title="Boutique IMS Home", page_icon="", layout="wide")
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
    
    logged_in_user = st.session_state["username"]
    user_role = config['credentials']['usernames'][logged_in_user]['roles'][0]
    st.session_state['user_role'] = user_role

    st.title("Boutique Management System")
    st.markdown(f"### Welcome back, **{st.session_state['name']}**! ✨")
    
    conn = get_db_connection()
    if not conn:
        st.error("Database connection failed. Please check your secrets.")
        st.stop()

    if user_role == "admin":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            df_stock = pd.read_sql("SELECT SUM(stocklevel) as total FROM inventory", conn)
            raw_stock = df_stock['total'].iloc[0]
            val = int(raw_stock) if pd.notna(raw_stock) else 0
            st.metric("Total Items on Shelves", f"{val:,}")
            
        with col2:
            df_con = pd.read_sql("SELECT COUNT(*) as count FROM contract WHERE enddate >= CURDATE()", conn)
            con_val = df_con['count'].iloc[0] if pd.notna(df_con['count'].iloc[0]) else 0
            st.metric("Active Contracts", con_val)
            
        with col3:
            df_perf = pd.read_sql("SELECT COUNT(*) as count FROM supplierperformance WHERE shippingspeed = 'fast'", conn)
            perf_val = df_perf['count'].iloc[0] if pd.notna(df_perf['count'].iloc[0]) else 0
            st.metric("Top Performing Suppliers", perf_val)

        st.markdown("---")
        st.subheader("Inventory Intelligence")
        
        try:
            df_alerts = pd.read_sql("SELECT COUNT(*) as count FROM lowstockalerts", conn)
            alert_count = df_alerts['count'].iloc[0] if pd.notna(df_alerts['count'].iloc[0]) else 0
            
            if alert_count > 0:
                st.error(f" **Urgent! Low Stock Alerts:** There are {alert_count} items currently below reorder points. Please review the Reports page.")
            else:
                st.success("**Stock Status:** All boutique inventory levels are currently healthy.")
        except Exception as e:
            st.info("Stock alerts are currently unavailable.")
            
        st.info("System access: Admin level. All financial and supplier data is visible.")

    else:
        st.markdown("---")
        st.subheader(" Supplier Portal")
        st.write(f"Hello {st.session_state['name']}, your access is restricted to your specific product associations.")
        
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
                st.warning(f"⚠️ **Stock Alert:** {my_alert_count} of the items you supply are running low in our warehouse.")
            else:
                st.success("Your supplied products are currently well-stocked.")
        except:
            st.write("Performance metrics are loading...")

        query = f"SELECT COUNT(*) as count FROM supplierperformance WHERE suppliername = '{st.session_state['name']}'"
        df_my_perf = pd.read_sql(query, conn)
        my_count = df_my_perf['count'].iloc[0] if not df_my_perf.empty else 0
        st.metric("Your Tracked Products", my_count)
        
        st.info("Navigate to the **Reports** tab to see your delivery lead times and speed analysis.")

    conn.close()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    
elif st.session_state["authentication_status"] is None:
    st.info("Welcome to the Boutique IMS. Please log in to manage inventory.")
    st.stop()