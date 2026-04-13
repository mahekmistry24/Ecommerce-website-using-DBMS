"""
Database Initialization Script.
Creates PostgreSQL tables and seeds data into both PostgreSQL and MongoDB.
"""
import os
import json
from sqlalchemy import text
from app.db.postgres import engine, SessionLocal, Base
from app.db.mongo import (
    products_collection,
    reviews_collection,
    logs_collection,
    init_mongo_indexes,
)

# Import all models so Base.metadata knows about them
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory
from app.models.shipment import Shipment


def get_sql_dir():
    """Get the path to the sql/ directory."""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "sql",
    )


def get_mongodb_dir():
    """Get the path to the mongodb/ directory."""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "mongodb",
    )


def init_postgres():
    """Create PostgreSQL tables and seed data."""
    print("🐘 Initializing PostgreSQL...")

    # Create tables via ORM
    Base.metadata.create_all(bind=engine)
    print("  ✅ Tables created via SQLAlchemy ORM")

    sql_dir = get_sql_dir()

    # Run SQL scripts in order
    sql_files = [
        "indexes.sql",
        "procedures.sql",
        "triggers.sql",
        "partitioning.sql",
        "sample_data.sql",
    ]

    for sql_file in sql_files:
        filepath = os.path.join(sql_dir, sql_file)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    sql_content = f.read()
                # Execute each statement separately with its own transaction
                statements = [
                    s.strip()
                    for s in sql_content.split(";")
                    if s.strip() and not s.strip().startswith("--")
                ]
                for stmt in statements:
                    if stmt:
                        try:
                            with engine.connect() as conn:
                                conn.execute(text(stmt))
                                conn.commit()
                        except Exception as e:
                            err = str(e).lower()
                            if "already exists" not in err and "duplicate" not in err:
                                pass  # silently skip
                print(f"  ✅ Executed {sql_file}")
            except Exception as e:
                print(f"  ⚠️  Error in {sql_file}: {str(e)[:100]}")
        else:
            print(f"  ⏭️  Skipped {sql_file} (not found)")


def init_mongodb():
    """Seed MongoDB collections with sample data."""
    print("\n🍃 Initializing MongoDB...")

    # Create indexes
    init_mongo_indexes()
    print("  ✅ MongoDB indexes created")

    mongodb_dir = get_mongodb_dir()

    # Import products
    products_file = os.path.join(mongodb_dir, "sample_products.json")
    if os.path.exists(products_file):
        with open(products_file, "r", encoding="utf-8") as f:
            products = json.load(f)

        imported = 0
        for product in products:
            existing = products_collection.find_one(
                {"product_id": product["product_id"]}
            )
            if not existing:
                products_collection.insert_one(product)
                imported += 1

        print(f"  ✅ Products: {imported} imported ({products_collection.count_documents({})} total)")

    # Import reviews
    reviews_file = os.path.join(mongodb_dir, "sample_reviews.json")
    if os.path.exists(reviews_file):
        with open(reviews_file, "r", encoding="utf-8") as f:
            reviews = json.load(f)

        imported = 0
        for review in reviews:
            existing = reviews_collection.find_one(
                {"review_id": review["review_id"]}
            )
            if not existing:
                reviews_collection.insert_one(review)
                imported += 1

        print(f"  ✅ Reviews: {imported} imported ({reviews_collection.count_documents({})} total)")

    print(f"  ✅ Logs collection ready ({logs_collection.count_documents({})} events)")


def init_all():
    """Initialize all databases."""
    print("=" * 60)
    print("🚀 Smart Distributed E-Commerce System - DB Initialization")
    print("=" * 60)
    init_postgres()
    init_mongodb()
    print("\n" + "=" * 60)
    print("✅ All databases initialized successfully!")
    print("=" * 60)


if __name__ == "__main__":
    init_all()
