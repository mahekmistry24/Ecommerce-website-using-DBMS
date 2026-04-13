"""
Stock Service: Warehouse stock allocation and management.
Demonstrates distributed inventory across multiple warehouses.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.inventory import Inventory
from app.models.warehouse import Warehouse


def get_product_stock(db: Session, product_id: str) -> list:
    """Get stock levels for a product across all warehouses."""
    results = (
        db.query(
            Inventory.inventory_id,
            Inventory.product_id,
            Inventory.warehouse_id,
            Inventory.quantity,
            Inventory.reserved_quantity,
            Inventory.last_updated,
            Warehouse.warehouse_name,
            Warehouse.city,
            Warehouse.state,
        )
        .join(Warehouse, Inventory.warehouse_id == Warehouse.warehouse_id)
        .filter(Inventory.product_id == product_id)
        .all()
    )

    return [
        {
            "inventory_id": r.inventory_id,
            "product_id": r.product_id,
            "warehouse_id": r.warehouse_id,
            "warehouse_name": r.warehouse_name,
            "city": r.city,
            "state": r.state,
            "quantity": r.quantity,
            "reserved_quantity": r.reserved_quantity,
            "available": r.quantity - r.reserved_quantity,
            "last_updated": r.last_updated.isoformat() if r.last_updated else None,
        }
        for r in results
    ]


def get_total_available_stock(db: Session, product_id: str) -> int:
    """Get total available stock across all warehouses."""
    result = (
        db.query(func.sum(Inventory.quantity - Inventory.reserved_quantity))
        .filter(Inventory.product_id == product_id)
        .scalar()
    )
    return result or 0


def find_best_warehouse(db: Session, product_id: str, quantity: int) -> int:
    """Find the warehouse with the most stock for the given product."""
    result = (
        db.query(Inventory)
        .join(Warehouse, Inventory.warehouse_id == Warehouse.warehouse_id)
        .filter(
            Inventory.product_id == product_id,
            (Inventory.quantity - Inventory.reserved_quantity) >= quantity,
            Warehouse.is_active == True,
        )
        .order_by((Inventory.quantity - Inventory.reserved_quantity).desc())
        .first()
    )
    return result.warehouse_id if result else None


def get_all_inventory(db: Session) -> list:
    """Get all inventory records with warehouse details."""
    results = (
        db.query(
            Inventory.inventory_id,
            Inventory.product_id,
            Inventory.warehouse_id,
            Inventory.quantity,
            Inventory.reserved_quantity,
            Inventory.last_updated,
            Warehouse.warehouse_name,
            Warehouse.city,
        )
        .join(Warehouse, Inventory.warehouse_id == Warehouse.warehouse_id)
        .order_by(Inventory.product_id)
        .all()
    )

    return [
        {
            "inventory_id": r.inventory_id,
            "product_id": r.product_id,
            "warehouse_id": r.warehouse_id,
            "warehouse_name": r.warehouse_name,
            "city": r.city,
            "quantity": r.quantity,
            "reserved_quantity": r.reserved_quantity,
            "available": r.quantity - r.reserved_quantity,
            "last_updated": r.last_updated.isoformat() if r.last_updated else None,
        }
        for r in results
    ]


def get_low_stock_alerts(db: Session, threshold: int = 20) -> list:
    """Get products with stock below threshold across any warehouse."""
    results = (
        db.query(
            Inventory.product_id,
            Inventory.warehouse_id,
            Inventory.quantity,
            Warehouse.warehouse_name,
            Warehouse.city,
        )
        .join(Warehouse, Inventory.warehouse_id == Warehouse.warehouse_id)
        .filter(Inventory.quantity <= threshold)
        .order_by(Inventory.quantity)
        .all()
    )

    return [
        {
            "product_id": r.product_id,
            "warehouse_id": r.warehouse_id,
            "warehouse_name": r.warehouse_name,
            "city": r.city,
            "quantity": r.quantity,
        }
        for r in results
    ]
