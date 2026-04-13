"""
SQLAlchemy ORM Model: Inventory
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.db.postgres import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(String(50), nullable=False, index=True)
    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.warehouse_id", ondelete="CASCADE"),
        nullable=False,
    )
    quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, default=0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("product_id", "warehouse_id", name="uq_product_warehouse"),
    )
