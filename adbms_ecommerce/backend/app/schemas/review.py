"""
Pydantic schemas for Review endpoints (MongoDB).
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    product_id: str
    user_id: int
    rating: int  # 1-5
    review_text: str


class ReviewResponse(BaseModel):
    review_id: str
    product_id: str
    user_id: int
    rating: int
    review_text: str
    helpful_votes: int = 0
    created_at: Optional[str] = None
