"""
Analytics Service: MongoDB aggregation pipelines + PostgreSQL query analysis.
Demonstrates: NoSQL aggregation, query optimization, EXPLAIN ANALYZE.
"""
from app.db.mongo import products_collection, reviews_collection, logs_collection
from sqlalchemy.orm import Session
from sqlalchemy import text


def get_top_rated_products(limit: int = 10) -> list:
    """Aggregation: Top-rated products."""
    pipeline = [
        {"$match": {"ratings_summary.review_count": {"$gte": 5}}},
        {"$project": {
            "_id": 0,
            "product_id": 1,
            "name": 1,
            "brand": 1,
            "category": 1,
            "price": 1,
            "avg_rating": "$ratings_summary.avg_rating",
            "review_count": "$ratings_summary.review_count",
        }},
        {"$sort": {"avg_rating": -1}},
        {"$limit": limit},
    ]
    return list(products_collection.aggregate(pipeline))


def get_category_stats() -> list:
    """Aggregation: Category-wise statistics."""
    pipeline = [
        {"$group": {
            "_id": "$category",
            "total_products": {"$sum": 1},
            "avg_price": {"$avg": "$price"},
            "avg_rating": {"$avg": "$ratings_summary.avg_rating"},
            "total_reviews": {"$sum": "$ratings_summary.review_count"},
            "min_price": {"$min": "$price"},
            "max_price": {"$max": "$price"},
        }},
        {"$sort": {"total_reviews": -1}},
    ]
    return list(products_collection.aggregate(pipeline))


def get_brand_stats() -> list:
    """Aggregation: Brand-wise statistics."""
    pipeline = [
        {"$group": {
            "_id": "$brand",
            "product_count": {"$sum": 1},
            "avg_price": {"$avg": "$price"},
            "total_reviews": {"$sum": "$ratings_summary.review_count"},
            "avg_rating": {"$avg": "$ratings_summary.avg_rating"},
        }},
        {"$sort": {"total_reviews": -1}},
    ]
    return list(products_collection.aggregate(pipeline))


def get_price_distribution() -> list:
    """Aggregation: Price distribution using buckets."""
    pipeline = [
        {"$bucket": {
            "groupBy": "$price",
            "boundaries": [0, 1000, 2000, 3000, 5000, 10000],
            "default": "10000+",
            "output": {
                "count": {"$sum": 1},
                "products": {"$push": "$name"},
                "avg_rating": {"$avg": "$ratings_summary.avg_rating"},
            },
        }},
    ]
    return list(products_collection.aggregate(pipeline))


def get_review_stats() -> list:
    """Aggregation: Review statistics per product."""
    pipeline = [
        {"$group": {
            "_id": "$product_id",
            "total_reviews": {"$sum": 1},
            "avg_rating": {"$avg": "$rating"},
            "max_rating": {"$max": "$rating"},
            "min_rating": {"$min": "$rating"},
        }},
        {"$sort": {"avg_rating": -1}},
    ]
    return list(reviews_collection.aggregate(pipeline))


def get_user_activity_stats() -> list:
    """Aggregation: User activity from logs."""
    pipeline = [
        {"$group": {
            "_id": {"user_id": "$user_id", "event_type": "$event_type"},
            "count": {"$sum": 1},
            "last_activity": {"$max": "$timestamp"},
        }},
        {"$group": {
            "_id": "$_id.user_id",
            "activities": {
                "$push": {
                    "event": "$_id.event_type",
                    "count": "$count",
                    "last": "$last_activity",
                }
            },
            "total_events": {"$sum": "$count"},
        }},
        {"$sort": {"total_events": -1}},
    ]
    return list(logs_collection.aggregate(pipeline))


def get_query_performance(db: Session) -> list:
    """
    Run EXPLAIN ANALYZE on sample queries to demonstrate query optimization.
    """
    queries = [
        {
            "name": "Orders by User (with index)",
            "sql": "EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 2",
        },
        {
            "name": "Inventory by Product (with index)",
            "sql": "EXPLAIN ANALYZE SELECT * FROM inventory WHERE product_id = 'P1001'",
        },
        {
            "name": "Orders by Date Range",
            "sql": "EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date >= '2026-01-01' AND order_date < '2026-04-01'",
        },
        {
            "name": "User by Email (with index)",
            "sql": "EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'mahekmistry@gmail.com'",
        },
        {
            "name": "Full Join: Orders + Items + Payments",
            "sql": """EXPLAIN ANALYZE
                SELECT o.order_id, o.status, o.total_amount, 
                       oi.product_id, oi.quantity, oi.unit_price,
                       p.payment_mode, p.payment_status
                FROM orders o
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN payments p ON o.order_id = p.order_id
                WHERE o.user_id = 2""",
        },
    ]

    results = []
    for q in queries:
        try:
            result = db.execute(text(q["sql"]))
            plan = [row[0] for row in result.fetchall()]
            results.append({
                "query_name": q["name"],
                "plan": plan,
            })
        except Exception as e:
            results.append({
                "query_name": q["name"],
                "error": str(e),
            })

    return results
