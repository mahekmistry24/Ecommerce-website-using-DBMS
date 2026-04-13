"""
SQLAlchemy ORM Model: Payment
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.postgres import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    payment_mode = Column(String(30), nullable=False)
    payment_status = Column(String(30), default="pending")
    amount = Column(Numeric(12, 2), nullable=False)
    payment_date = Column(DateTime, server_default=func.now())
    transaction_ref = Column(String(100))

    # Relationships
    order = relationship("Order", back_populates="payment")
