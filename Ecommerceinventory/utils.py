from turtle import pd
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
        st.error(f"Error: {e}")
        return None
def check_low_stock_alerts():
    conn = get_db_connection()
    try:
        query = "SELECT COUNT(*) as count FROM lowStockAlerts"
        df = pd.read_sql(query, conn)
        return df['count'][0]
    except:
        return 0
    finally:
        conn.close()