import streamlit as st
import pandas as pd
from datetime import datetime
from utils import get_db_connection, check_low_stock_alerts
from style_utils import apply_theme 

st.set_page_config(page_title="Order Boutique", layout="wide")
apply_theme()

alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"{alert_count} Low Stock Alerts!")
else:
    st.sidebar.info("☁️ Stock levels normal")

st.title("Order Management")

conn = get_db_connection()

with st.expander("Create New Restock Order"):
    with st.form("new_order_form"):
        suppliers = pd.read_sql("select supplierid, name from supplier", conn) #
        products = pd.read_sql("select productid, name from product", conn) #
        
        col1, col2, col3 = st.columns(3)
        with col1:
            sel_sup = st.selectbox("Supplier", suppliers['name'])
        with col2:
            sel_prod = st.selectbox("Product", products['name'])
        with col3:
            qty = st.number_input("Quantity", min_value=1)
            
        if st.form_submit_button("Confirm Purchase Order"):
            cursor = conn.cursor()
            try:
                sup_id = suppliers[suppliers['name'] == sel_sup]['supplierid'].values[0]
                prod_id = products[products['name'] == sel_prod]['productid'].values[0]
                
                cursor.execute("INSERT INTO orders (supplierid, orderstatus, ordereddate) VALUES (%s, 'pending', CURDATE())", (int(sup_id),))
                order_id = cursor.lastrowid
                
                cursor.execute("INSERT INTO orderitem (orderid, productid, quantity) VALUES (%s, %s, %s)", (order_id, int(prod_id), qty))
                
                conn.commit()
                st.info(f"Order #{order_id} recorded for {sel_prod}!")
            except Exception as e:
                st.error(f"Failed to create order: {e}")
            finally:
                cursor.close()

st.markdown("---")

st.subheader("Receive Deliveries")
query_pending = """
    SELECT o.orderid, s.name as supplier, p.name as product, oi.quantity
    FROM orders o
    JOIN supplier s ON o.supplierid = s.supplierid
    JOIN orderitem oi ON o.orderid = oi.orderid
    JOIN product p ON oi.productid = p.productid
    WHERE o.orderstatus = 'pending'
"""
df_pending = pd.read_sql(query_pending, conn)

if not df_pending.empty:
    st.dataframe(df_pending, use_container_width=True)
    
    selected_order = st.selectbox("Select Order ID to Mark as Received", df_pending['orderid'])
    
    if st.button("Receive Delivery & Add to Stock"):
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
            st.info(f"Boutique inventory updated for Order #{selected_order}!") 
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
else:
    st.write("All orders have arrived! Your boutique is full. ")

conn.close()