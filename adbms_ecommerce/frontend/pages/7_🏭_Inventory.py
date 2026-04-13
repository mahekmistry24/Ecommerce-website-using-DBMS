"""
Inventory Page: View stock levels across warehouses.
Demonstrates distributed database inventory management.
"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get, api_post

st.set_page_config(page_title="Inventory | Smart E-Commerce", page_icon="🏭", layout="wide")

st.markdown("## 🏭 Distributed Inventory Management")

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Product Stock", "⚠️ Low Stock Alerts"])

with tab1:
    st.markdown("### 📦 All Inventory Records")
    data = api_get("/inventory")
    if "error" not in data:
        inventory = data.get("inventory", [])
        if inventory:
            df = pd.DataFrame(inventory)
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total SKUs", df["product_id"].nunique())
            with col2:
                st.metric("Total Stock", f"{df['quantity'].sum():,}")
            with col3:
                st.metric("Total Available", f"{df['available'].sum():,}")

            st.dataframe(
                df[["product_id", "warehouse_name", "city", "quantity", "reserved_quantity", "available"]],
                use_container_width=True,
                hide_index=True,
            )

            # Warehouse distribution chart
            st.markdown("### 📊 Stock by Warehouse")
            wh_stock = df.groupby("warehouse_name")["quantity"].sum().reset_index()
            st.bar_chart(wh_stock.set_index("warehouse_name"))
        else:
            st.info("No inventory data found.")

with tab2:
    st.markdown("### 🔍 Check Product Stock Across Warehouses")
    product_id = st.text_input("Enter Product ID", value="P1001")

    if product_id:
        stock_data = api_get(f"/inventory/product/{product_id}")
        if "error" not in stock_data:
            st.metric("Total Available Stock", stock_data.get("total_available", 0))

            warehouses = stock_data.get("warehouses", [])
            if warehouses:
                df = pd.DataFrame(warehouses)
                st.dataframe(
                    df[["warehouse_name", "city", "state", "quantity", "reserved_quantity", "available"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.warning("No stock found for this product.")

    # Update stock
    st.markdown("---")
    st.markdown("### 🔄 Update Stock")
    col1, col2, col3 = st.columns(3)
    with col1:
        upd_pid = st.text_input("Product ID", key="upd_pid")
    with col2:
        upd_wid = st.number_input("Warehouse ID", min_value=1, value=1)
    with col3:
        upd_qty = st.number_input("New Quantity", min_value=0, value=100)

    if st.button("✅ Update Stock"):
        if upd_pid:
            result = api_post("/inventory/update", {
                "product_id": upd_pid,
                "warehouse_id": upd_wid,
                "quantity": upd_qty,
            })
            if "error" not in result:
                st.success("✅ Stock updated!")
            else:
                st.error(f"Failed: {result.get('error', '')}")

with tab3:
    st.markdown("### ⚠️ Low Stock Alerts")
    threshold = st.slider("Alert Threshold", 5, 100, 20)

    alerts = api_get(f"/inventory/low-stock", {"threshold": threshold})
    if "error" not in alerts:
        alert_list = alerts.get("alerts", [])
        st.warning(f"**{len(alert_list)} items below stock threshold of {threshold}**")

        if alert_list:
            df = pd.DataFrame(alert_list)
            st.dataframe(df, use_container_width=True, hide_index=True)
