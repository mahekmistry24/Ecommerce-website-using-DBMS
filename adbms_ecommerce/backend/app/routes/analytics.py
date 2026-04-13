"""
Analytics routes: Aggregation pipelines and query performance.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.services.analytics_service import (
    get_top_rated_products,
    get_category_stats,
    get_brand_stats,
    get_price_distribution,
    get_review_stats,
    get_user_activity_stats,
    get_query_performance,
)
from app.db.mongo import logs_collection, products_collection, reviews_collection
from sqlalchemy import text

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/top-products")
def top_products(limit: int = 10):
    """Get top-rated products using MongoDB aggregation."""
    return {"top_products": get_top_rated_products(limit)}


@router.get("/category-stats")
def category_stats():
    """Get category-wise statistics."""
    stats = get_category_stats()
    for s in stats:
        s["avg_price"] = round(s.get("avg_price", 0), 2)
        s["avg_rating"] = round(s.get("avg_rating", 0), 1)
    return {"categories": stats}


@router.get("/brand-stats")
def brand_stats():
    """Get brand-wise statistics."""
    stats = get_brand_stats()
    for s in stats:
        s["avg_price"] = round(s.get("avg_price", 0), 2)
        s["avg_rating"] = round(s.get("avg_rating", 0), 1)
    return {"brands": stats}


@router.get("/price-distribution")
def price_distribution():
    """Get price distribution using MongoDB bucket aggregation."""
    return {"distribution": get_price_distribution()}


@router.get("/review-stats")
def review_stats():
    """Get review statistics per product."""
    stats = get_review_stats()
    for s in stats:
        s["avg_rating"] = round(s.get("avg_rating", 0), 1)
    return {"review_stats": stats}


@router.get("/user-activity")
def user_activity():
    """Get user activity analytics from event logs."""
    return {"activity": get_user_activity_stats()}


@router.get("/query-performance")
def query_performance(db: Session = Depends(get_db)):
    """Run EXPLAIN ANALYZE on sample queries."""
    return {"queries": get_query_performance(db)}


@router.get("/dashboard-summary")
def dashboard_summary(db: Session = Depends(get_db)):
    """Get a summary of all key metrics for the dashboard."""
    # MongoDB counts
    total_products = products_collection.count_documents({})
    total_reviews = reviews_collection.count_documents({})
    total_events = logs_collection.count_documents({})

    # PostgreSQL counts
    total_users = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    total_orders = db.execute(text("SELECT COUNT(*) FROM orders")).scalar()
    total_revenue = db.execute(
        text("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'cancelled'")
    ).scalar()
    pending_orders = db.execute(
        text("SELECT COUNT(*) FROM orders WHERE status = 'pending'")
    ).scalar()
    total_warehouses = db.execute(text("SELECT COUNT(*) FROM warehouses")).scalar()

    return {
        "total_products": total_products,
        "total_users": total_users,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "total_reviews": total_reviews,
        "pending_orders": pending_orders,
        "total_warehouses": total_warehouses,
        "total_events": total_events,
    }
