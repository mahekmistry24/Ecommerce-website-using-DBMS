"""
Cart & Checkout Page: Place orders.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get, api_post

st.set_page_config(page_title="Cart & Checkout | Smart E-Commerce", page_icon="🛒", layout="wide")

st.markdown("## 🛒 Cart & Checkout")

# Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# Add to cart section
st.markdown("### ➕ Add Product to Cart")
col1, col2 = st.columns([2, 1])

with col1:
    product_id = st.text_input("Product ID", placeholder="e.g., P1001")

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1)

if product_id and st.button("🔍 Look Up & Add to Cart"):
    product = api_get(f"/products/{product_id}")
    if "error" not in product and "detail" not in product:
        st.session_state.cart.append({
            "product_id": product["product_id"],
            "product_name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity,
        })
        st.success(f"✅ Added {product['name']} x{quantity} to cart!")
    else:
        st.error("Product not found")

# Quick add buttons
st.markdown("### ⚡ Quick Add Popular Products")
popular = api_get("/products", {"limit": 6, "sort_by": "rating", "sort_order": -1})
if "error" not in popular:
    cols = st.columns(3)
    for idx, p in enumerate(popular.get("products", [])[:6]):
        with cols[idx % 3]:
            if st.button(f"➕ {p['name'][:25]}... (₹{p['price']:,.0f})", key=f"quick_{p['product_id']}"):
                st.session_state.cart.append({
                    "product_id": p["product_id"],
                    "product_name": p["name"],
                    "unit_price": p["price"],
                    "quantity": 1,
                })
                st.rerun()

# Show cart
st.markdown("---")
st.markdown("### 🛍️ Your Cart")

if not st.session_state.cart:
    st.info("Your cart is empty. Add products above.")
else:
    total = 0
    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        with col1:
            st.write(f"**{item['product_name']}**")
        with col2:
            st.write(f"₹{item['unit_price']:,.0f}")
        with col3:
            st.write(f"x{item['quantity']}")
        with col4:
            subtotal = item['unit_price'] * item['quantity']
            st.write(f"₹{subtotal:,.0f}")
            total += subtotal
        with col5:
            if st.button("🗑️", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

    st.markdown(f"### 💰 Total: ₹{total:,.2f}")

    if st.button("🗑️ Clear Cart"):
        st.session_state.cart = []
        st.rerun()

    # Checkout form
    st.markdown("---")
    st.markdown("### 📝 Checkout")

    # Get users for selection
    users = api_get("/auth/users")
    if "error" not in users:
        user_options = {f"{u['name']} ({u['email']})": u["user_id"] for u in users}
        selected_user = st.selectbox("Select User", list(user_options.keys()))
        user_id = user_options[selected_user]
    else:
        user_id = st.number_input("User ID", min_value=1, value=1)

    shipping_address = st.text_area("Shipping Address", placeholder="Enter full address...")
    payment_mode = st.selectbox("Payment Mode", ["upi", "credit_card", "debit_card", "net_banking", "cod", "wallet"])

    if st.button("✅ Place Order", type="primary", use_container_width=True):
        if not shipping_address:
            st.error("Please enter a shipping address")
        else:
            order_data = {
                "user_id": user_id,
                "items": st.session_state.cart,
                "shipping_address": shipping_address,
                "payment_mode": payment_mode,
            }
            result = api_post("/orders", order_data)
            if "error" not in result and "detail" not in result:
                st.balloons()
                st.success(f"🎉 Order placed successfully! Order ID: {result.get('order_id')}")
                st.info(f"Total: ₹{result.get('total_amount', 0):,.2f} | Status: {result.get('status')}")
                st.session_state.cart = []
            else:
                st.error(f"Order failed: {result.get('detail', result.get('error', 'Unknown error'))}")
