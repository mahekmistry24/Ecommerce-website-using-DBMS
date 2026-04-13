"""
My Orders Page: View order history and details.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get, get_xml_content

st.set_page_config(page_title="My Orders | Smart E-Commerce", page_icon="📋", layout="wide")

st.markdown("## 📋 Order History")

# User selection
users = api_get("/auth/users")
if "error" not in users:
    user_options = {f"{u['name']} ({u['email']})": u["user_id"] for u in users}
    selected_user = st.selectbox("Select User", list(user_options.keys()))
    user_id = user_options[selected_user]
else:
    user_id = st.number_input("User ID", min_value=1, value=2)

# Fetch orders
data = api_get(f"/orders/user/{user_id}")
if "error" in data:
    st.error(f"Error: {data['error']}")
else:
    orders = data.get("orders", [])
    st.markdown(f"**{len(orders)} orders found**")

    for order in orders:
        status_emoji = {
            "pending": "⏳", "confirmed": "✅", "processing": "🔄",
            "shipped": "🚚", "delivered": "📦", "cancelled": "❌"
        }
        emoji = status_emoji.get(order["status"], "📋")

        with st.expander(
            f"{emoji} Order #{order['order_id']} — ₹{order['total_amount']:,.2f} — "
            f"{order['status'].upper()} — {order.get('order_date', '')[:10]}"
        ):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**📋 Order Details**")
                st.write(f"**Order ID:** {order['order_id']}")
                st.write(f"**Date:** {order.get('order_date', 'N/A')[:19]}")
                st.write(f"**Status:** {order['status']}")
                st.write(f"**Address:** {order.get('shipping_address', 'N/A')}")

            with col2:
                st.markdown("**💳 Payment**")
                if order.get("payment"):
                    pay = order["payment"]
                    st.write(f"**Mode:** {pay['payment_mode']}")
                    st.write(f"**Status:** {pay['payment_status']}")
                    st.write(f"**Ref:** {pay.get('transaction_ref', 'N/A')}")

            with col3:
                st.markdown("**🚚 Shipment**")
                if order.get("shipment"):
                    ship = order["shipment"]
                    st.write(f"**Courier:** {ship.get('courier_name', 'N/A')}")
                    st.write(f"**Tracking:** {ship.get('tracking_number', 'N/A')}")
                    st.write(f"**Status:** {ship.get('shipment_status', 'N/A')}")
                    if ship.get("estimated_delivery"):
                        st.write(f"**ETA:** {ship['estimated_delivery']}")

            # Order items
            st.markdown("**📦 Items:**")
            for item in order.get("items", []):
                st.write(
                    f"  • {item['product_name']} — Qty: {item['quantity']} — "
                    f"₹{item['unit_price']:,.2f} each — Subtotal: ₹{item['quantity'] * item['unit_price']:,.2f}"
                )

            # XML Export
            if st.button(f"📄 Export as XML", key=f"xml_{order['order_id']}"):
                xml_content = get_xml_content(f"/api/xml/order/{order['order_id']}")
                st.download_button(
                    "💾 Download XML",
                    xml_content,
                    f"order_{order['order_id']}.xml",
                    "application/xml",
                    key=f"dl_{order['order_id']}",
                )
