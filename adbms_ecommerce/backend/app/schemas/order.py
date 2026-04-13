"""
Pydantic schemas for Order endpoints.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]
    shipping_address: str
    payment_mode: str  # credit_card, debit_card, upi, net_banking, cod, wallet
    notes: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: str  # pending, confirmed, processing, shipped, delivered, cancelled


class OrderItemResponse(BaseModel):
    order_item_id: int
    product_id: str
    product_name: Optional[str] = None
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class PaymentResponse(BaseModel):
    payment_id: int
    payment_mode: str
    payment_status: str
    amount: float
    payment_date: Optional[datetime] = None
    transaction_ref: Optional[str] = None

    class Config:
        from_attributes = True


class ShipmentResponse(BaseModel):
    shipment_id: int
    warehouse_id: Optional[int] = None
    courier_name: Optional[str] = None
    tracking_number: Optional[str] = None
    shipment_status: str
    estimated_delivery: Optional[str] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    order_date: Optional[datetime] = None
    status: str
    total_amount: float
    shipping_address: Optional[str] = None
    items: List[OrderItemResponse] = []
    payment: Optional[PaymentResponse] = None
    shipment: Optional[ShipmentResponse] = None

    class Config:
        from_attributes = True
