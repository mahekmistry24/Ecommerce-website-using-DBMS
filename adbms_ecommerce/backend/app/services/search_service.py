"""
Search Service: MongoDB product search with filters and text search.
"""
from app.db.mongo import products_collection


def search_products(
    query: str = None,
    category: str = None,
    brand: str = None,
    min_price: float = None,
    max_price: float = None,
    tags: list = None,
    sort_by: str = "name",
    sort_order: int = 1,
    page: int = 1,
    limit: int = 20,
) -> dict:
    """
    Search products in MongoDB with flexible filters.
    Demonstrates NoSQL query flexibility.
    """
    # Build filter
    filter_query = {}

    if query:
        filter_query["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"brand": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}},
            {"tags": {"$regex": query, "$options": "i"}},
        ]

    if category:
        filter_query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    if brand:
        filter_query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}

    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        filter_query["price"] = price_filter

    if tags:
        filter_query["tags"] = {"$in": tags}

    # Sort mapping
    sort_map = {
        "name": "name",
        "price": "price",
        "rating": "ratings_summary.avg_rating",
        "reviews": "ratings_summary.review_count",
    }
    sort_field = sort_map.get(sort_by, "name")

    # Execute query with pagination
    skip = (page - 1) * limit
    total = products_collection.count_documents(filter_query)
    
    cursor = (
        products_collection.find(filter_query, {"_id": 0})
        .sort(sort_field, sort_order)
        .skip(skip)
        .limit(limit)
    )

    products = list(cursor)

    return {
        "products": products,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if limit > 0 else 0,
    }


def get_categories() -> list:
    """Get all distinct product categories."""
    return products_collection.distinct("category")


def get_brands() -> list:
    """Get all distinct product brands."""
    return products_collection.distinct("brand")
