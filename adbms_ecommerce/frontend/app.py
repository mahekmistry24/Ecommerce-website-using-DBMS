"""
Smart Distributed E-Commerce Database System
Main Streamlit Application
"""
import streamlit as st

st.set_page_config(
    page_title="Smart E-Commerce | ADBMS Project",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }

    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: white;
    }

    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛒 Smart Distributed E-Commerce System</h1>
        <p>Advanced Database Management System Project | PostgreSQL + MongoDB + FastAPI</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎓 ADBMS Project")
        st.markdown("---")
        st.info("Navigate using the pages in the sidebar ☝️")

        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Dashboard Summary
    from utils import api_get
    summary = api_get("/analytics/dashboard-summary")

    if "error" in summary:
        st.error(f"⚠️ Backend Connection Error: {summary['error']}")
        st.info("Make sure the FastAPI backend is running on port 8000")
        return

    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('total_products', 0)}</div>
            <div class="metric-label">📦 Products</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('total_orders', 0)}</div>
            <div class="metric-label">🛍️ Orders</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('total_users', 0)}</div>
            <div class="metric-label">👥 Users</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{summary.get('total_revenue', 0):,.0f}</div>
            <div class="metric-label">💰 Revenue</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Second row of metrics
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('total_reviews', 0)}</div>
            <div class="metric-label">⭐ Reviews</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('pending_orders', 0)}</div>
            <div class="metric-label">⏳ Pending Orders</div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('total_warehouses', 0)}</div>
            <div class="metric-label">🏭 Warehouses</div>
        </div>
        """, unsafe_allow_html=True)

    with col8:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary.get('total_events', 0)}</div>
            <div class="metric-label">📊 Events Logged</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#888;'>Smart Distributed E-Commerce System | "
        "ADBMS Project 2026 | Built with PostgreSQL, MongoDB, FastAPI & Streamlit</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
