"""
XML utilities for order export and product import.
ADBMS: Demonstrates XML and semi-structured data handling.
"""
from lxml import etree
from datetime import datetime


def order_to_xml(order_data: dict) -> str:
    """Convert an order dictionary to XML format."""
    root = etree.Element("Order")
    root.set("order_id", str(order_data.get("order_id", "")))
    root.set("date", str(order_data.get("order_date", "")))

    # Customer info
    customer = etree.SubElement(root, "Customer")
    customer.set("user_id", str(order_data.get("user_id", "")))
    if order_data.get("customer_name"):
        name_el = etree.SubElement(customer, "Name")
        name_el.text = order_data["customer_name"]

    # Shipping address
    shipping = etree.SubElement(root, "ShippingAddress")
    shipping.text = order_data.get("shipping_address", "")

    # Order items
    items_el = etree.SubElement(root, "Items")
    for item in order_data.get("items", []):
        item_el = etree.SubElement(items_el, "Item")
        item_el.set("product_id", str(item.get("product_id", "")))

        name_el = etree.SubElement(item_el, "ProductName")
        name_el.text = str(item.get("product_name", ""))

        qty_el = etree.SubElement(item_el, "Quantity")
        qty_el.text = str(item.get("quantity", 0))

        price_el = etree.SubElement(item_el, "UnitPrice")
        price_el.text = str(item.get("unit_price", 0))

        subtotal = etree.SubElement(item_el, "Subtotal")
        subtotal.text = str(
            round(item.get("quantity", 0) * item.get("unit_price", 0), 2)
        )

    # Payment
    if order_data.get("payment"):
        pay_el = etree.SubElement(root, "Payment")
        pay = order_data["payment"]
        mode = etree.SubElement(pay_el, "Mode")
        mode.text = str(pay.get("payment_mode", ""))
        status = etree.SubElement(pay_el, "Status")
        status.text = str(pay.get("payment_status", ""))
        txn = etree.SubElement(pay_el, "TransactionRef")
        txn.text = str(pay.get("transaction_ref", ""))

    # Total
    total = etree.SubElement(root, "TotalAmount")
    total.text = str(order_data.get("total_amount", 0))

    # Status
    status_el = etree.SubElement(root, "Status")
    status_el.text = order_data.get("status", "")

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()


def parse_product_xml(xml_string: str) -> list:
    """Parse an XML product feed and return a list of product dicts."""
    root = etree.fromstring(xml_string.encode() if isinstance(xml_string, str) else xml_string)
    products = []

    for product_el in root.findall(".//Product"):
        product = {
            "product_id": product_el.get("id", ""),
            "name": _get_text(product_el, "Name"),
            "brand": _get_text(product_el, "Brand"),
            "category": _get_text(product_el, "Category"),
            "price": float(_get_text(product_el, "Price") or 0),
            "description": _get_text(product_el, "Description"),
            "tags": [],
            "attributes": {},
            "in_stock": True,
            "ratings_summary": {"avg_rating": 0, "review_count": 0},
        }

        # Parse tags
        tags_el = product_el.find("Tags")
        if tags_el is not None:
            for tag in tags_el.findall("Tag"):
                if tag.text:
                    product["tags"].append(tag.text.strip())

        # Parse attributes
        attrs_el = product_el.find("Attributes")
        if attrs_el is not None:
            for attr in attrs_el:
                product["attributes"][attr.tag] = attr.text

        products.append(product)

    return products


def _get_text(element, tag):
    """Helper to get text content of a child element."""
    child = element.find(tag)
    return child.text.strip() if child is not None and child.text else ""
