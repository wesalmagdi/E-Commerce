import streamlit as st
import pandas as pd
from utils import get_db_connection
from style_utils import apply_theme 

st.set_page_config(page_title="Report generation", layout="wide")
apply_theme()

def color_speed(val):
    if val == 'fast':
        return 'color: #2E4053; font-weight: bold;'
    elif val == 'average':
        return 'color: #2E4053;' 
    elif val == 'slow':
        return 'color: #E74C3C; font-weight: bold;'
    return ''

def main():
    st.title("Management Reports")
    
    conn = get_db_connection()
    if conn is None:
        st.error("Database connection failed.")
        return

    user_role = st.session_state.get("roles", ["supplier"])[0]
    user_display_name = st.session_state.get("name", "User")

    if user_role == "admin":
        st.subheader("Full Performance Overview (Admin Access)")
        query = "SELECT * FROM supplierperformance"
    else:
        st.subheader(f"Performance Tags for {user_display_name}")
        query = f"SELECT * FROM supplierperformance WHERE suppliername = '{user_display_name}'"

    try:
        df = pd.read_sql(query, conn)

        if not df.empty:
            st.write("Current Supplier Analytics:")
            st.dataframe(
                df.style.applymap(color_speed, subset=['shippingspeed']),
                use_container_width=True
            )

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Report as CSV",
                data=csv,
                file_name='supplier_performance_report.csv',
                mime='text/csv',
            )
        else:
            st.info("No performance data available. Check if your products have lead times assigned.")
    except Exception as e:
        st.error(f"Error loading report: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if st.session_state.get("authentication_status"):
        main()
    else:
        st.warning("Please log in on the Home page to view reports.")