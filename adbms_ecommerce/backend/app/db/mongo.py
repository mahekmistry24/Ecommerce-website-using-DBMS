"""
MongoDB connection using PyMongo.
Demonstrates: NoSQL document store for flexible schema data.
"""
from pymongo import MongoClient, ASCENDING, TEXT
from app.config import settings

# Create MongoDB client
client = MongoClient(settings.MONGO_URL)

# Database reference
mongo_db = client[settings.MONGO_DB_NAME]

# Collection references
products_collection = mongo_db["products"]
reviews_collection = mongo_db["reviews"]
logs_collection = mongo_db["logs"]


def init_mongo_indexes():
    """Create indexes on MongoDB collections for query optimization."""
    # Product indexes
    products_collection.create_index([("product_id", ASCENDING)], unique=True)
    products_collection.create_index([("category", ASCENDING)])
    products_collection.create_index([("brand", ASCENDING)])
    products_collection.create_index([("price", ASCENDING)])
    products_collection.create_index([("name", TEXT), ("brand", TEXT), ("category", TEXT)])

    # Review indexes
    reviews_collection.create_index([("product_id", ASCENDING)])
    reviews_collection.create_index([("user_id", ASCENDING)])
    reviews_collection.create_index([("rating", ASCENDING)])

    # Log indexes
    logs_collection.create_index([("user_id", ASCENDING)])
    logs_collection.create_index([("event_type", ASCENDING)])
    logs_collection.create_index([("timestamp", ASCENDING)])


def get_mongo_db():
    """Return the MongoDB database instance."""
    return mongo_db
