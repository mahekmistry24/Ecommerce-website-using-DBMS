"""
Analytics Page: MongoDB aggregation pipelines and query performance.
Demonstrates: NoSQL aggregation, query optimization, EXPLAIN ANALYZE.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import api_get

st.set_page_config(page_title="Analytics | Smart E-Commerce", page_icon="📈", layout="wide")

st.markdown("## 📈 Analytics & Query Performance")

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Top Products", "📊 Category Stats", "🏷️ Brand Analysis",
    "💰 Price Distribution"
])

with tab1:
    st.markdown("### 🏆 Top-Rated Products (MongoDB Aggregation)")
    top = api_get("/analytics/top-products", {"limit": 10})
    if "error" not in top:
        products = top.get("top_products", [])
        if products:
            df = pd.DataFrame(products)
            
            fig = px.bar(
                df, x="name", y="avg_rating", color="category",
                title="Top Rated Products by Average Rating",
                labels={"avg_rating": "Average Rating", "name": "Product"},
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                df[["product_id", "name", "brand", "category", "avg_rating", "review_count"]],
                use_container_width=True, hide_index=True,
            )

with tab2:
    st.markdown("### 📊 Category-wise Statistics (MongoDB Aggregation)")
    cat_data = api_get("/analytics/category-stats")
    if "error" not in cat_data:
        categories = cat_data.get("categories", [])
        if categories:
            df = pd.DataFrame(categories)
            df = df.rename(columns={"_id": "category"})

            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    df, names="category", values="total_products",
                    title="Products by Category",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(
                    df, x="category", y="total_reviews",
                    title="Reviews by Category",
                    color="avg_rating",
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### 🏷️ Brand Analysis (MongoDB Aggregation)")
    brand_data = api_get("/analytics/brand-stats")
    if "error" not in brand_data:
        brands = brand_data.get("brands", [])
        if brands:
            df = pd.DataFrame(brands)
            df = df.rename(columns={"_id": "brand"})

            fig = px.scatter(
                df, x="avg_price", y="avg_rating", size="total_reviews",
                color="brand", title="Brand Analysis: Price vs Rating vs Popularity",
                labels={"avg_price": "Avg Price (₹)", "avg_rating": "Avg Rating"},
                size_max=40,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df, use_container_width=True, hide_index=True)

with tab4:
    st.markdown("### 💰 Price Distribution (MongoDB Bucket Aggregation)")
    price_data = api_get("/analytics/price-distribution")
    if "error" not in price_data:
        distribution = price_data.get("distribution", [])
        if distribution:
            labels = []
            counts = []
            for d in distribution:
                bucket = d.get("_id")
                if isinstance(bucket, (int, float)):
                    labels.append(f"₹{int(bucket)}+")
                else:
                    labels.append(str(bucket))
                counts.append(d.get("count", 0))

            fig = go.Figure(data=[go.Bar(
                x=labels, y=counts,
                marker_color=["#667eea", "#764ba2", "#f093fb", "#f5576c", "#fda085", "#a8edea"],
            )])
            fig.update_layout(
                title="Products by Price Range",
                xaxis_title="Price Range",
                yaxis_title="Number of Products",
            )
            st.plotly_chart(fig, use_container_width=True)

            for d in distribution:
                bucket = d.get("_id")
                label = f"₹{int(bucket)}+" if isinstance(bucket, (int, float)) else str(bucket)
                with st.expander(f"{label} ({d.get('count', 0)} products)"):
                    st.write(", ".join(d.get("products", [])))
                    st.write(f"Avg Rating: {d.get('avg_rating', 0):.1f}")


