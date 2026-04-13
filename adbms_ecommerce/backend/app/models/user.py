"""
SQLAlchemy ORM Model: User
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.postgres import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15))
    password_hash = Column(String, nullable=False)
    role = Column(String(20), default="customer")
    created_at = Column(DateTime, server_default=func.now())
