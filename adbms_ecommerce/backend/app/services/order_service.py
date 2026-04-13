"""
Order Service: Business logic for order placement.
Handles transactional order creation across PostgreSQL tables.
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.shipment import Shipment
from app.models.inventory import Inventory
from app.utils.logger import log_event


def create_order(db: Session, order_data: dict) -> Order:
    """
    Create a complete order with items, payment, and shipment.
    Uses PostgreSQL transaction to ensure atomicity.
    """
    try:
        # 1. Calculate total
        total = sum(
            item["quantity"] * item["unit_price"] for item in order_data["items"]
        )

        # 2. Create order
        order = Order(
            user_id=order_data["user_id"],
            status="confirmed",
            total_amount=total,
            shipping_address=order_data.get("shipping_address", ""),
            notes=order_data.get("notes", ""),
        )
        db.add(order)
        db.flush()  # Get order_id

        # 3. Add order items and reduce inventory
        warehouse_id = None
        for item_data in order_data["items"]:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item_data["product_id"],
                product_name=item_data.get("product_name", ""),
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
            )
            db.add(order_item)

            # Find warehouse with stock and reduce inventory
            inv = (
                db.query(Inventory)
                .filter(
                    Inventory.product_id == item_data["product_id"],
                    Inventory.quantity >= item_data["quantity"],
                )
                .order_by(Inventory.quantity.desc())
                .first()
            )

            if inv:
                inv.quantity -= item_data["quantity"]
                inv.last_updated = datetime.now(timezone.utc)
                warehouse_id = inv.warehouse_id

        # 4. Create payment record
        txn_ref = f"TXN-{order.order_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        payment = Payment(
            order_id=order.order_id,
            payment_mode=order_data.get("payment_mode", "upi"),
            payment_status="completed" if order_data.get("payment_mode") != "cod" else "pending",
            amount=total,
            transaction_ref=txn_ref,
        )
        db.add(payment)

        # 5. Create shipment record
        shipment = Shipment(
            order_id=order.order_id,
            warehouse_id=warehouse_id or 1,
            courier_name="FastShip Express",
            tracking_number=f"TRACK-{order.order_id}-{datetime.now().strftime('%Y%m%d')}",
            shipment_status="preparing",
            estimated_delivery=(datetime.now() + timedelta(days=5)).date(),
        )
        db.add(shipment)

        # 6. Commit entire transaction
        db.commit()
        db.refresh(order)

        # 7. Log event to MongoDB
        log_event(
            "ORDER_PLACED",
            user_id=order_data["user_id"],
            metadata={
                "order_id": order.order_id,
                "total": float(total),
                "items_count": len(order_data["items"]),
            },
        )

        return order

    except Exception as e:
        db.rollback()
        raise e


def update_order_status(db: Session, order_id: int, new_status: str) -> Order:
    """Update order status (triggers audit log via PostgreSQL trigger)."""
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return None
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
