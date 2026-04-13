"""
Reviews Page: View and submit product reviews.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get, api_post

st.set_page_config(page_title="Reviews | Smart E-Commerce", page_icon="⭐", layout="wide")

st.markdown("## ⭐ Product Reviews")

tab1, tab2 = st.tabs(["📖 View Reviews", "✍️ Write a Review"])

with tab1:
    product_id = st.text_input("Enter Product ID to view reviews", value="P1001", key="view_pid")

    if product_id:
        # Show product info
        product = api_get(f"/products/{product_id}")
        if "error" not in product and "detail" not in product:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {product.get('name', '')}")
                st.write(f"**Brand:** {product.get('brand', '')} | **Category:** {product.get('category', '')}")
                st.write(f"**Price:** ₹{product.get('price', 0):,.0f}")
            with col2:
                rating = product.get("ratings_summary", {})
                avg = rating.get("avg_rating", 0)
                count = rating.get("review_count", 0)
                st.metric("Average Rating", f"⭐ {avg}/5")
                st.metric("Total Reviews", count)

            # Rating distribution
            if rating:
                st.markdown("**Rating Distribution**")
                for star in [5, 4, 3, 2, 1]:
                    key = f"{'five' if star==5 else 'four' if star==4 else 'three' if star==3 else 'two' if star==2 else 'one'}_star"
                    cnt = rating.get(key, 0)
                    pct = (cnt / count * 100) if count > 0 else 0
                    st.progress(pct / 100, text=f"{'⭐' * star} — {cnt} ({pct:.0f}%)")

        # Fetch reviews
        reviews_data = api_get(f"/reviews/{product_id}")
        if "error" not in reviews_data:
            reviews = reviews_data.get("reviews", [])
            st.markdown(f"### 💬 Reviews ({reviews_data.get('total', 0)})")

            for review in reviews:
                stars = "⭐" * review.get("rating", 0)
                st.markdown(f"""
                <div style="background:white; border:1px solid #eee; border-radius:10px; padding:1rem; margin-bottom:0.8rem; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                    <div style="display:flex; justify-content:space-between;">
                        <span>{stars}</span>
                        <span style="color:#888; font-size:0.8rem;">User #{review.get('user_id', '')} • {str(review.get('created_at', ''))[:10]}</span>
                    </div>
                    <p style="margin-top:0.5rem;">{review.get('review_text', '')}</p>
                    <span style="color:#888; font-size:0.8rem;">👍 {review.get('helpful_votes', 0)} found helpful</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No reviews yet for this product.")

with tab2:
    st.markdown("### ✍️ Write a Review")

    review_product_id = st.text_input("Product ID", value="P1001", key="write_pid")
    review_user_id = st.number_input("Your User ID", min_value=1, value=2)
    review_rating = st.slider("Rating", 1, 5, 5)
    review_text = st.text_area("Your Review", placeholder="Share your experience with this product...")

    if st.button("📝 Submit Review", type="primary"):
        if review_text:
            result = api_post("/reviews", {
                "product_id": review_product_id,
                "user_id": review_user_id,
                "rating": review_rating,
                "review_text": review_text,
            })
            if "error" not in result and "detail" not in result:
                st.success(f"✅ Review submitted! ID: {result.get('review_id')}")
            else:
                st.error(f"Failed: {result.get('detail', result.get('error', ''))}")
        else:
            st.warning("Please write a review before submitting.")
