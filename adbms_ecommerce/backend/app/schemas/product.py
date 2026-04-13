"""
Pydantic schemas for Product endpoints (MongoDB).
"""
from pydantic import BaseModel
from typing import Optional, Dict, List, Any


class ProductCreate(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    subcategory: Optional[str] = None
    price: float
    mrp: Optional[float] = None
    discount_percent: Optional[int] = 0
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = {}
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []
    in_stock: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    mrp: Optional[float] = None
    discount_percent: Optional[int] = None
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    in_stock: Optional[bool] = None


class ProductSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    tags: Optional[List[str]] = None
    sort_by: Optional[str] = "name"  # name, price, rating
    sort_order: Optional[int] = 1    # 1=asc, -1=desc
    page: int = 1
    limit: int = 20
