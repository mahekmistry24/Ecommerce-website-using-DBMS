"""
Review routes: Add and list product reviews (MongoDB).
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from app.db.mongo import reviews_collection, products_collection
from app.schemas.review import ReviewCreate
from app.utils.logger import log_event

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.get("/{product_id}")
def get_reviews(product_id: str, page: int = 1, limit: int = 20):
    """Get reviews for a product."""
    skip = (page - 1) * limit
    total = reviews_collection.count_documents({"product_id": product_id})
    reviews = list(
        reviews_collection.find({"product_id": product_id}, {"_id": 0})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )

    # Get rating distribution
    pipeline = [
        {"$match": {"product_id": product_id}},
        {"$group": {
            "_id": "$rating",
            "count": {"$sum": 1},
        }},
    ]
    distribution = {r["_id"]: r["count"] for r in reviews_collection.aggregate(pipeline)}

    return {
        "product_id": product_id,
        "reviews": reviews,
        "total": total,
        "page": page,
        "rating_distribution": distribution,
    }


@router.post("", status_code=201)
def add_review(review_data: ReviewCreate):
    """Add a new review and update product rating summary."""
    # Generate review ID
    count = reviews_collection.count_documents({})
    review_id = f"R{count + 100:03d}"

    review_dict = {
        "review_id": review_id,
        "product_id": review_data.product_id,
        "user_id": review_data.user_id,
        "rating": review_data.rating,
        "review_text": review_data.review_text,
        "helpful_votes": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    reviews_collection.insert_one(review_dict)

    # Update product rating summary
    pipeline = [
        {"$match": {"product_id": review_data.product_id}},
        {"$group": {
            "_id": None,
            "avg_rating": {"$avg": "$rating"},
            "review_count": {"$sum": 1},
            "five_star": {"$sum": {"$cond": [{"$eq": ["$rating", 5]}, 1, 0]}},
            "four_star": {"$sum": {"$cond": [{"$eq": ["$rating", 4]}, 1, 0]}},
            "three_star": {"$sum": {"$cond": [{"$eq": ["$rating", 3]}, 1, 0]}},
            "two_star": {"$sum": {"$cond": [{"$eq": ["$rating", 2]}, 1, 0]}},
            "one_star": {"$sum": {"$cond": [{"$eq": ["$rating", 1]}, 1, 0]}},
        }},
    ]
    stats = list(reviews_collection.aggregate(pipeline))
    if stats:
        s = stats[0]
        products_collection.update_one(
            {"product_id": review_data.product_id},
            {"$set": {
                "ratings_summary": {
                    "avg_rating": round(s["avg_rating"], 1),
                    "review_count": s["review_count"],
                    "five_star": s["five_star"],
                    "four_star": s["four_star"],
                    "three_star": s["three_star"],
                    "two_star": s["two_star"],
                    "one_star": s["one_star"],
                }
            }},
        )

    log_event("REVIEW_ADDED", user_id=review_data.user_id, product_id=review_data.product_id)

    return {"message": "Review added successfully", "review_id": review_id}
