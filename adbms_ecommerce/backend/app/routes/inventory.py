"""
Inventory routes: Stock management across warehouses.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.models.inventory import Inventory
from app.models.warehouse import Warehouse
from app.schemas.inventory import InventoryUpdate, WarehouseCreate, WarehouseResponse
from app.services.stock_service import (
    get_product_stock,
    get_total_available_stock,
    get_all_inventory,
    get_low_stock_alerts,
)
from app.utils.logger import log_event

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("")
def list_all_inventory(db: Session = Depends(get_db)):
    """Get all inventory records with warehouse details."""
    return {"inventory": get_all_inventory(db)}


@router.get("/product/{product_id}")
def get_stock_by_product(product_id: str, db: Session = Depends(get_db)):
    """Get stock levels for a product across all warehouses."""
    stock = get_product_stock(db, product_id)
    total = get_total_available_stock(db, product_id)
    return {
        "product_id": product_id,
        "total_available": total,
        "warehouses": stock,
    }


@router.get("/low-stock")
def low_stock_alerts(threshold: int = 20, db: Session = Depends(get_db)):
    """Get products with stock below threshold."""
    alerts = get_low_stock_alerts(db, threshold)
    return {"threshold": threshold, "alerts": alerts, "count": len(alerts)}


@router.post("/update")
def update_inventory(data: InventoryUpdate, db: Session = Depends(get_db)):
    """Update or create inventory record."""
    inv = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == data.product_id,
            Inventory.warehouse_id == data.warehouse_id,
        )
        .first()
    )

    if inv:
        inv.quantity = data.quantity
    else:
        inv = Inventory(
            product_id=data.product_id,
            warehouse_id=data.warehouse_id,
            quantity=data.quantity,
        )
        db.add(inv)

    db.commit()
    log_event(
        "INVENTORY_UPDATE",
        product_id=data.product_id,
        metadata={"warehouse_id": data.warehouse_id, "quantity": data.quantity},
    )
    return {"message": "Inventory updated successfully"}


# =================== WAREHOUSE ENDPOINTS ===================

@router.get("/warehouses", response_model=list[WarehouseResponse])
def list_warehouses(db: Session = Depends(get_db)):
    """Get all warehouses."""
    warehouses = db.query(Warehouse).all()
    return [WarehouseResponse.model_validate(w) for w in warehouses]


@router.post("/warehouses", status_code=201)
def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db)):
    """Create a new warehouse."""
    warehouse = Warehouse(**data.model_dump())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return {
        "message": "Warehouse created successfully",
        "warehouse_id": warehouse.warehouse_id,
    }
