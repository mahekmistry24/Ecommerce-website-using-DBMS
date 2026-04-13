"""
XML API routes: Export orders to XML, import products from XML.
ADBMS: Demonstrates XML and semi-structured data handling.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from app.db.postgres import get_db
from app.db.mongo import products_collection
from app.models.order import Order
from app.models.user import User
from app.utils.xml_utils import order_to_xml, parse_product_xml

router = APIRouter(prefix="/api/xml", tags=["XML"])


@router.get("/order/{order_id}")
def export_order_xml(order_id: int, db: Session = Depends(get_db)):
    """Export an order as XML document."""
    order = (
        db.query(Order)
        .options(joinedload(Order.items), joinedload(Order.payment))
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Get customer name
    user = db.query(User).filter(User.user_id == order.user_id).first()

    order_data = {
        "order_id": order.order_id,
        "user_id": order.user_id,
        "customer_name": user.name if user else "",
        "order_date": order.order_date.isoformat() if order.order_date else "",
        "status": order.status,
        "total_amount": float(order.total_amount) if order.total_amount else 0,
        "shipping_address": order.shipping_address or "",
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
            }
            for item in order.items
        ],
        "payment": {
            "payment_mode": order.payment.payment_mode,
            "payment_status": order.payment.payment_status,
            "transaction_ref": order.payment.transaction_ref,
        } if order.payment else None,
    }

    xml_content = order_to_xml(order_data)
    return Response(content=xml_content, media_type="application/xml")


@router.post("/products/import")
async def import_products_xml(file: UploadFile = File(...)):
    """Import products from an XML file."""
    if not file.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="File must be XML")

    content = await file.read()
    try:
        products = parse_product_xml(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid XML: {str(e)}")

    imported = 0
    for product in products:
        existing = products_collection.find_one({"product_id": product["product_id"]})
        if not existing:
            products_collection.insert_one(product)
            imported += 1

    return {
        "message": f"Imported {imported} products from XML",
        "total_in_file": len(products),
        "newly_imported": imported,
    }
