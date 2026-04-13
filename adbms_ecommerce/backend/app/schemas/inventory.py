"""
Pydantic schemas for Inventory endpoints.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InventoryUpdate(BaseModel):
    product_id: str
    warehouse_id: int
    quantity: int


class InventoryResponse(BaseModel):
    inventory_id: int
    product_id: str
    warehouse_id: int
    quantity: int
    reserved_quantity: int
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class WarehouseCreate(BaseModel):
    warehouse_name: str
    city: str
    state: str
    pincode: Optional[str] = None
    capacity: int = 10000


class WarehouseResponse(BaseModel):
    warehouse_id: int
    warehouse_name: str
    city: str
    state: str
    pincode: Optional[str] = None
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True
