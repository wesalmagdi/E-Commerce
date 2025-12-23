import pandas as pd 
import mysql.connector
import streamlit as st

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"]
        )
        return conn
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def check_low_stock_alerts():
    conn = get_db_connection()
    if conn is None:
        return 0
    try:
        query = "SELECT COUNT(*) as count FROM lowstockalerts" 
        df = pd.read_sql(query, conn)
        return int(df['count'].iloc[0]) if not df.empty else 0
    except Exception as e:
        print(f"Database Query Error: {e}") 
        return 0
    finally:
        conn.close()