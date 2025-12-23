import streamlit as st
import pandas as pd
from utils import get_db_connection
from datetime import datetime
from style_utils import apply_theme

st.set_page_config(page_title="Contracts & Suppliers", layout="wide")
apply_theme()

st.title("Supplier Contract Management")
st.markdown("---")

def get_data():
    conn = get_db_connection()
    query = """
    select s.name, s.email, c.startdate, c.enddate, c.penalties 
    from supplier s 
    left join contract c on s.supplierid = c.supplierid
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

col1, col2, col3 = st.columns(3)
data = get_data()
col1.metric("Total Suppliers", len(data['name'].unique()))
col2.metric("Active Contracts", data['enddate'].notnull().sum())
col3.metric("Urgent Renewals", 1) 

with st.expander("Register New Contract / Restock Terms"):
    with st.form("contract_form"):
        conn = get_db_connection()
        suppliers = pd.read_sql("select supplierid, name from supplier", conn)
        
        c_sup = st.selectbox("Select Supplier", suppliers['name'])
        c_start = st.date_input("Contract Start Date")
        c_end = st.date_input("Contract End Date")
        c_terms = st.text_area("Restock Terms & Penalties", placeholder="e.g., 5% penalty for delays over 3 days")
        
        if st.form_submit_button("Finalize Contract"):
            sup_id = suppliers[suppliers['name'] == c_sup]['supplierid'].values[0]
            cursor = conn.cursor()
            cursor.execute("""
                insert into contract (supplierid, startdate, enddate, penalties, createdat)
                values (%s, %s, %s, %s, %s)
            """, (int(sup_id), c_start, c_end, c_terms, datetime.now()))
            conn.commit()
            st.success(f"Contract for {c_sup} recorded!")
        conn.close()

st.subheader("Current Supplier Network")
st.dataframe(data, use_container_width=True)