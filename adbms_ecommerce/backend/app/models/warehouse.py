"""
SQLAlchemy ORM Model: Warehouse
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.postgres import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    warehouse_name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    pincode = Column(String(10))
    capacity = Column(Integer, default=10000)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
