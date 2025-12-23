import streamlit as st
import pandas as pd
from utils import get_db_connection, check_low_stock_alerts
from style_utils import apply_theme

st.set_page_config(page_title="Inventory Management", layout="wide")
apply_theme()

# 1. Auth Guard
if "user_role" not in st.session_state or st.session_state["user_role"] != "admin":
    st.error("Access Denied. Inventory management is restricted to Admin users.")
    st.stop()

# 2. Sidebar Alert (Sync with Database View)
alert_count = check_low_stock_alerts()
if alert_count > 0:
    st.sidebar.error(f"🚨 {alert_count} Low Stock Alerts!")
else:
    st.sidebar.success("✅ Stock levels normal")

st.title("Warehouse Stock Tracking")

conn = get_db_connection()

# 3. Pull Current Inventory Data
# We select directly from the inventory table joined with products
query_main = """
    SELECT i.productid, p.name as product_name, i.stocklevel, i.reorderpoint 
    FROM inventory i
    JOIN product p ON i.productid = p.productid
"""
df_inv = pd.read_sql(query_main, conn)

# 4. Pull ONLY Low Stock items from your SQL VIEW
# This ensures the GUI matches your SQL Workbench results exactly
df_low_stock_view = pd.read_sql("SELECT * FROM lowstockalerts", conn)
low_stock_count = len(df_low_stock_view)

# 5. Display Metrics
col1, col2 = st.columns(2)
col1.metric("Total Unique Products", len(df_inv))
# Metric now uses the actual count from the Database View
col2.metric(
    label="Low Stock Items", 
    value=low_stock_count, 
    delta=f"{low_stock_count} Alert(s)" if low_stock_count > 0 else None,
    delta_color="inverse"
)

if low_stock_count > 0:
    st.warning(f"⚠️ Action Required: {low_stock_count} items are at or below reorder points.")
    # Show only names from the view results
    st.dataframe(df_low_stock_view, use_container_width=True)
else:
    st.success("✨ All stock levels are healthy.")

st.markdown("---")

# 6. Manage Reorder Points (Editable Table)
st.subheader("Manage Reorder Points")
edited_df = st.data_editor(
    df_inv, 
    column_config={
        "productid": None, # Hide ID from user
        "product_name": st.column_config.Column("Product", disabled=True),
        "stocklevel": st.column_config.Column("Current Stock", disabled=True),
        "reorderpoint": st.column_config.NumberColumn("Reorder Point", min_value=0)
    },
    use_container_width=True,
    key="inventory_editor"
)

# 7. Update Logic
if st.button("Save Inventory Changes"):
    cursor = conn.cursor()
    try:
        # Check for changes in the data_editor
        if "inventory_editor" in st.session_state:
            # edited_rows contains {index: {column: new_value}}
            changes = st.session_state["inventory_editor"].get("edited_rows", {})
            
            for index, change in changes.items():
                if "reorderpoint" in change:
                    new_val = change["reorderpoint"]
                    # Map index back to productid
                    pid = df_inv.iloc[index]['productid']
                    
                    # FIXED SQL SYNTAX: Removed the comma after 'inventory'
                    cursor.execute(
                        "UPDATE inventory SET reorderpoint = %s WHERE productid = %s",
                        (int(new_val), int(pid))
                    )
            
            conn.commit()
            st.success("Database updated successfully!")
            st.rerun() 
    except Exception as e:
        st.error(f"Failed to update database: {e}")
    finally:
        cursor.close()

conn.close()