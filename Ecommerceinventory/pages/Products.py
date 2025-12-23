import streamlit as st
import pandas as pd
from utils import get_db_connection, check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="Inventory Management", layout="wide")
apply_theme()

# Auth Guard
if "user_role" not in st.session_state or st.session_state["user_role"] != "admin":
    st.error("Access Denied.")
    st.stop()

st.title("Warehouse Stock Tracking")
conn = get_db_connection()

# --- DATABASE UPDATE LOGIC ---
if st.button("Save Inventory Changes"):
    cursor = conn.cursor()
    try:
        # Accessing the data from the data_editor session state
        # Note: data_editor returns a dict of changes
        if "inventory_editor" in st.session_state:
            edited_rows = st.session_state["inventory_editor"].get("edited_rows", {})
            
            # We need the full dataframe to map indices back to product IDs
            # This matches the 'df_inv' query below
            temp_df = pd.read_sql("SELECT productid FROM inventory", conn)

            for index, changes in edited_rows.items():
                if "reorderpoint" in changes:
                    new_val = changes["reorderpoint"]
                    pid = temp_df.iloc[index]["productid"]
                    
                    # FIXED: Removed the comma after 'inventory'
                    cursor.execute(
                        "UPDATE inventory SET reorderpoint = %s WHERE productid = %s",
                        (int(new_val), int(pid))
                    )
            
            conn.commit()
            st.success("Changes saved! Refreshing alerts...")
            st.rerun()
    except Exception as e:
        st.error(f"Save failed: {e}")
    finally:
        cursor.close()

# --- METRICS & ALERTS ---
# We call this AFTER the potential update so it's fresh
alert_count = check_low_stock_alerts()

if alert_count > 0:
    st.sidebar.error(f"🚨 {alert_count} Low Stock Alerts!")
else:
    st.sidebar.success("✅ Stock levels normal")

col1, col2 = st.columns(2)

# Get the main data
query_all = """
    SELECT i.productid, p.name as product_name, i.stocklevel, i.reorderpoint 
    FROM inventory i
    JOIN product p ON i.productid = p.productid
"""
df_inv = pd.read_sql(query_all, conn)

# Use your View for the Metric (Consistency with your SQL file)
df_low_stock_from_view = pd.read_sql("SELECT * FROM lowstockalerts", conn)

col1.metric("Total Unique Products", len(df_inv))
col2.metric("Low Stock Items", len(df_low_stock_from_view), delta=-len(df_low_stock_from_view) if len(df_low_stock_from_view) > 0 else 0, delta_color="inverse")

# --- DATA DISPLAY ---
if not df_low_stock_from_view.empty:
    st.warning(f"Action Required: {len(df_low_stock_from_view)} items need restocking.")
    # Joining with product names for the warning display
    alert_display = df_inv[df_inv['productid'].isin(df_low_stock_from_view['productid'])]
    st.dataframe(alert_display[['product_name', 'stocklevel', 'reorderpoint']], use_container_width=True)

st.markdown("---")
st.subheader("Edit Reorder Points")

# Data Editor
st.data_editor(
    df_inv, 
    column_config={
        "productid": None, # Hide ID
        "product_name": st.column_config.Column("Product Name", disabled=True),
        "stocklevel": st.column_config.Column("Current Stock", disabled=True),
        "reorderpoint": st.column_config.NumberColumn("Reorder Point", min_value=0)
    },
    use_container_width=True,
    key="inventory_editor"
)

conn.close()