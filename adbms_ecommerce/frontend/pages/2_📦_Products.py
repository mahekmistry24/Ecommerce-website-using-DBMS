"""
Products Page: Browse, search, and filter the product catalog.
Data source: MongoDB
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get

st.set_page_config(page_title="Products | Smart E-Commerce", page_icon="📦", layout="wide")

st.markdown("""
<style>
    .product-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .product-name { font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin-bottom: 0.3rem; }
    .product-brand { font-size: 0.85rem; color: #666; }
    .product-price { font-size: 1.3rem; font-weight: 700; color: #667eea; }
    .product-mrp { font-size: 0.85rem; color: #999; text-decoration: line-through; }
    .product-discount { font-size: 0.8rem; color: #27ae60; font-weight: 600; }
    .product-rating { font-size: 0.9rem; color: #f39c12; }
    .category-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        background: #e8f4f8;
        color: #2980b9;
        margin-right: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📦 Product Catalog")
st.markdown("*Browse products from our catalog*")

# Filters
with st.sidebar:
    st.markdown("### 🔍 Filters")

    # Get categories and brands
    cats_data = api_get("/products/categories")
    brands_data = api_get("/products/brands")

    categories = cats_data.get("categories", []) if "error" not in cats_data else []
    brands = brands_data.get("brands", []) if "error" not in brands_data else []

    selected_category = st.selectbox("Category", ["All"] + sorted(categories))
    selected_brand = st.selectbox("Brand", ["All"] + sorted(brands))

    col1, col2 = st.columns(2)
    with col1:
        min_price = st.number_input("Min Price ₹", min_value=0, value=0, step=100)
    with col2:
        max_price = st.number_input("Max Price ₹", min_value=0, value=10000, step=100)

    sort_by = st.selectbox("Sort By", ["name", "price", "rating", "reviews"])
    sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)

    st.markdown("---")
    search_query = st.text_input("🔎 Search Products", placeholder="e.g., headphones, cotton...")

# Build params
params = {
    "page": 1,
    "limit": 50,
    "sort_by": sort_by,
    "sort_order": 1 if sort_order == "Ascending" else -1,
}
if selected_category != "All":
    params["category"] = selected_category
if selected_brand != "All":
    params["brand"] = selected_brand
if min_price > 0:
    params["min_price"] = min_price
if max_price < 10000:
    params["max_price"] = max_price

# Fetch products
if search_query:
    params["q"] = search_query
    data = api_get("/products/search", params)
else:
    data = api_get("/products", params)

if "error" in data:
    st.error(f"Error: {data['error']}")
else:
    products = data.get("products", [])
    total = data.get("total", 0)

    st.markdown(f"**Showing {len(products)} of {total} products**")

    # Product grid
    cols = st.columns(3)
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            rating = product.get("ratings_summary", {})
            avg_r = rating.get("avg_rating", 0)
            rev_count = rating.get("review_count", 0)
            stars = "⭐" * int(avg_r) + "☆" * (5 - int(avg_r))

            discount = product.get("discount_percent", 0)
            mrp = product.get("mrp", product.get("price", 0))

            st.markdown(f"""
            <div class="product-card">
                <span class="category-tag">{product.get('category', '')}</span>
                <span class="category-tag">{product.get('subcategory', '')}</span>
                <div class="product-name">{product.get('name', '')}</div>
                <div class="product-brand">{product.get('brand', '')}</div>
                <div style="margin-top: 0.5rem;">
                    <span class="product-price">₹{product.get('price', 0):,.0f}</span>
                    <span class="product-mrp">₹{mrp:,.0f}</span>
                    <span class="product-discount">{discount}% off</span>
                </div>
                <div class="product-rating">{stars} {avg_r} ({rev_count} reviews)</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📋 Details"):
                st.write(product.get("description", ""))
                if product.get("attributes"):
                    for k, v in product["attributes"].items():
                        val_str = ", ".join(map(str, v)) if isinstance(v, list) else str(v)
                        st.markdown(f"- **{k.capitalize()}**: {val_str}")
                if product.get("tags"):
                    st.write("**Tags:** " + ", ".join(product["tags"]))
