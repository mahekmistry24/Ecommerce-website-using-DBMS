"""
Admin Dashboard Page: Manage products, orders, and warehouses.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get, api_post, api_put, api_delete

st.set_page_config(page_title="Admin Dashboard | Smart E-Commerce", page_icon="📊", layout="wide")

st.markdown("## 📊 Admin Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["📦 Add Product", "🏭 Warehouses", "📋 All Orders", "👥 Users"])

with tab1:
    st.markdown("### ➕ Add New Product")

    col1, col2 = st.columns(2)
    with col1:
        pid = st.text_input("Product ID*", placeholder="e.g., P5001")
        name = st.text_input("Product Name*", placeholder="e.g., Wireless Earbuds")
        brand = st.text_input("Brand*", placeholder="e.g., Samsung")
        category = st.selectbox("Category*", ["Electronics", "Clothing", "Books", "Beauty", "Food", "Fitness"])
        subcategory = st.text_input("Subcategory", placeholder="e.g., Audio")

    with col2:
        price = st.number_input("Price (₹)*", min_value=1, value=999)
        mrp = st.number_input("MRP (₹)", min_value=1, value=1499)
        discount = st.number_input("Discount %", min_value=0, max_value=99, value=30)
        description = st.text_area("Description", placeholder="Product description...")
        tags = st.text_input("Tags (comma-separated)", placeholder="wireless, bluetooth, audio")

    if st.button("✅ Add Product", type="primary"):
        if pid and name and brand:
            product_data = {
                "product_id": pid,
                "name": name,
                "brand": brand,
                "category": category,
                "subcategory": subcategory,
                "price": price,
                "mrp": mrp,
                "discount_percent": discount,
                "description": description,
                "tags": [t.strip() for t in tags.split(",") if t.strip()],
                "in_stock": True,
            }
            result = api_post("/products", product_data)
            if "error" not in result and "detail" not in result:
                st.success(f"✅ Product {pid} added successfully!")
            else:
                st.error(f"Failed: {result.get('detail', result.get('error', ''))}")
        else:
            st.warning("Please fill all required fields (*)")

with tab2:
    st.markdown("### 🏭 Warehouses")

    # List warehouses
    warehouses = api_get("/inventory/warehouses")
    if "error" not in warehouses:
        import pandas as pd
        df = pd.DataFrame(warehouses)
        if not df.empty:
            st.dataframe(df, use_container_width=True)

    st.markdown("### ➕ Add New Warehouse")
    col1, col2 = st.columns(2)
    with col1:
        wh_name = st.text_input("Warehouse Name")
        wh_city = st.text_input("City")
        wh_state = st.text_input("State")
    with col2:
        wh_pincode = st.text_input("Pincode")
        wh_capacity = st.number_input("Capacity", min_value=100, value=10000)

    if st.button("➕ Add Warehouse"):
        if wh_name and wh_city and wh_state:
            result = api_post("/inventory/warehouses", {
                "warehouse_name": wh_name,
                "city": wh_city,
                "state": wh_state,
                "pincode": wh_pincode,
                "capacity": wh_capacity,
            })
            if "error" not in result:
                st.success(f"✅ Warehouse added! ID: {result.get('warehouse_id')}")
                st.rerun()
            else:
                st.error(f"Failed: {result.get('error', '')}")

with tab3:
    st.markdown("### 📋 All Orders")

    orders_data = api_get("/orders")
    if "error" not in orders_data:
        orders = orders_data.get("orders", [])
        if orders:
            import pandas as pd
            df = pd.DataFrame(orders)
            st.dataframe(df, use_container_width=True)

            # Update order status
            st.markdown("### 🔄 Update Order Status")
            col1, col2 = st.columns(2)
            with col1:
                order_id = st.number_input("Order ID", min_value=1, value=1)
            with col2:
                new_status = st.selectbox("New Status", [
                    "pending", "confirmed", "processing", "shipped", "delivered", "cancelled"
                ])

            if st.button("🔄 Update Status"):
                result = api_put(f"/orders/{order_id}/status", {"status": new_status})
                if "error" not in result:
                    st.success(f"✅ Order {order_id} updated to {new_status}")
                    st.rerun()
                else:
                    st.error(f"Failed: {result.get('error', '')}")

with tab4:
    st.markdown("### 👥 Registered Users")
    users = api_get("/auth/users")
    if "error" not in users:
        import pandas as pd
        df = pd.DataFrame(users)
        st.dataframe(df, use_container_width=True)
    else:
        st.error(f"Error: {users.get('error', '')}")
