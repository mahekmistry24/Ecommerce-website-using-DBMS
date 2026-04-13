"""
MongoDB event logger.
Logs user actions for analytics and audit trails.
"""
from datetime import datetime, timezone
from app.db.mongo import logs_collection


def log_event(event_type: str, user_id: int = None, product_id: str = None, metadata: dict = None):
    """
    Log an event to MongoDB logs collection.
    
    Event types: PRODUCT_VIEW, ORDER_PLACED, USER_LOGIN, USER_REGISTER,
                 SEARCH, REVIEW_ADDED, CART_UPDATE, INVENTORY_UPDATE
    """
    log_entry = {
        "event_type": event_type,
        "user_id": user_id,
        "product_id": product_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {}
    }
    logs_collection.insert_one(log_entry)
