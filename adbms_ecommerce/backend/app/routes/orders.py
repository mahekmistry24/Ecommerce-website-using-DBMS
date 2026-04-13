"""
Order routes: Create orders, view order history, update status.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.postgres import get_db
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.shipment import Shipment
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.services.order_service import create_order, update_order_status

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("", status_code=201)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Place a new order with items, payment, and shipment."""
    try:
        order = create_order(db, order_data.model_dump())
        return {
            "message": "Order placed successfully",
            "order_id": order.order_id,
            "total_amount": float(order.total_amount),
            "status": order.status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")


@router.get("/user/{user_id}")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """Get order history for a user."""
    orders = (
        db.query(Order)
        .options(
            joinedload(Order.items),
            joinedload(Order.payment),
            joinedload(Order.shipment),
        )
        .filter(Order.user_id == user_id)
        .order_by(Order.order_date.desc())
        .all()
    )

    result = []
    for order in orders:
        order_dict = {
            "order_id": order.order_id,
            "user_id": order.user_id,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "status": order.status,
            "total_amount": float(order.total_amount) if order.total_amount else 0,
            "shipping_address": order.shipping_address,
            "items": [
                {
                    "order_item_id": item.order_item_id,
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                }
                for item in order.items
            ],
            "payment": {
                "payment_id": order.payment.payment_id,
                "payment_mode": order.payment.payment_mode,
                "payment_status": order.payment.payment_status,
                "amount": float(order.payment.amount),
                "transaction_ref": order.payment.transaction_ref,
            } if order.payment else None,
            "shipment": {
                "shipment_id": order.shipment.shipment_id,
                "warehouse_id": order.shipment.warehouse_id,
                "courier_name": order.shipment.courier_name,
                "tracking_number": order.shipment.tracking_number,
                "shipment_status": order.shipment.shipment_status,
                "estimated_delivery": str(order.shipment.estimated_delivery) if order.shipment.estimated_delivery else None,
            } if order.shipment else None,
        }
        result.append(order_dict)

    return {"orders": result, "total": len(result)}


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a single order by ID."""
    order = (
        db.query(Order)
        .options(
            joinedload(Order.items),
            joinedload(Order.payment),
            joinedload(Order.shipment),
        )
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order.order_id,
        "user_id": order.user_id,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "status": order.status,
        "total_amount": float(order.total_amount) if order.total_amount else 0,
        "shipping_address": order.shipping_address,
        "items": [
            {
                "order_item_id": item.order_item_id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
            }
            for item in order.items
        ],
        "payment": {
            "payment_id": order.payment.payment_id,
            "payment_mode": order.payment.payment_mode,
            "payment_status": order.payment.payment_status,
            "amount": float(order.payment.amount),
            "transaction_ref": order.payment.transaction_ref,
        } if order.payment else None,
        "shipment": {
            "shipment_id": order.shipment.shipment_id,
            "warehouse_id": order.shipment.warehouse_id,
            "courier_name": order.shipment.courier_name,
            "tracking_number": order.shipment.tracking_number,
            "shipment_status": order.shipment.shipment_status,
        } if order.shipment else None,
    }


@router.put("/{order_id}/status")
def change_order_status(
    order_id: int, status_data: OrderStatusUpdate, db: Session = Depends(get_db)
):
    """Update order status (triggers audit log via PostgreSQL trigger)."""
    order = update_order_status(db, order_id, status_data.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": f"Order {order_id} status updated to {status_data.status}"}


@router.get("")
def get_all_orders(db: Session = Depends(get_db)):
    """Get all orders (admin)."""
    orders = (
        db.query(Order)
        .options(joinedload(Order.items), joinedload(Order.payment))
        .order_by(Order.order_date.desc())
        .all()
    )

    result = []
    for order in orders:
        result.append({
            "order_id": order.order_id,
            "user_id": order.user_id,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "status": order.status,
            "total_amount": float(order.total_amount) if order.total_amount else 0,
            "items_count": len(order.items),
            "payment_mode": order.payment.payment_mode if order.payment else None,
            "payment_status": order.payment.payment_status if order.payment else None,
        })

    return {"orders": result, "total": len(result)}
