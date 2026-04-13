"""
SQLAlchemy ORM Model: Shipment
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"))
    courier_name = Column(String(100))
    tracking_number = Column(String(100))
    shipment_status = Column(String(30), default="preparing")
    estimated_delivery = Column(Date)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)

    # Relationships
    order = relationship("Order", back_populates="shipment")
