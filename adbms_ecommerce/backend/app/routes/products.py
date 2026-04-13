"""
Product routes: CRUD and search using MongoDB.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.db.mongo import products_collection
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.search_service import search_products, get_categories, get_brands
from app.utils.logger import log_event
from datetime import datetime, timezone

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("")
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "name",
    sort_order: Optional[int] = 1,
):
    """List all products with optional filters."""
    result = search_products(
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        limit=limit,
    )
    return result


@router.get("/search")
def search(
    q: str = Query(..., min_length=1),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    tags: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Search products by text query with filters."""
    tag_list = tags.split(",") if tags else None
    result = search_products(
        query=q,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        tags=tag_list,
        page=page,
        limit=limit,
    )
    log_event("SEARCH", metadata={"query": q, "results": result["total"]})
    return result


@router.get("/categories")
def list_categories():
    """Get all product categories."""
    return {"categories": get_categories()}


@router.get("/brands")
def list_brands():
    """Get all product brands."""
    return {"brands": get_brands()}


@router.get("/{product_id}")
def get_product(product_id: str, user_id: Optional[int] = None):
    """Get a single product by ID."""
    product = products_collection.find_one(
        {"product_id": product_id}, {"_id": 0}
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    log_event("PRODUCT_VIEW", user_id=user_id, product_id=product_id)
    return product


@router.post("", status_code=201)
def create_product(product: ProductCreate):
    """Add a new product to the catalog."""
    # Check if product_id already exists
    existing = products_collection.find_one({"product_id": product.product_id})
    if existing:
        raise HTTPException(status_code=400, detail="Product ID already exists")

    product_dict = product.model_dump()
    product_dict["created_at"] = datetime.now(timezone.utc).isoformat()
    product_dict["ratings_summary"] = {
        "avg_rating": 0,
        "review_count": 0,
        "five_star": 0,
        "four_star": 0,
        "three_star": 0,
        "two_star": 0,
        "one_star": 0,
    }

    products_collection.insert_one(product_dict)
    return {"message": "Product created successfully", "product_id": product.product_id}


@router.put("/{product_id}")
def update_product(product_id: str, update_data: ProductUpdate):
    """Update an existing product."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = products_collection.update_one(
        {"product_id": product_id}, {"$set": update_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product updated successfully"}


@router.delete("/{product_id}")
def delete_product(product_id: str):
    """Delete a product."""
    result = products_collection.delete_one({"product_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
