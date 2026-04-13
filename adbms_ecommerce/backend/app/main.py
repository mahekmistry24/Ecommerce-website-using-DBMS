"""
Smart Distributed E-Commerce Database System
FastAPI Main Application Entry Point

Technologies: PostgreSQL + MongoDB + FastAPI
ADBMS Project: Hybrid relational + NoSQL architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.init_db import init_all

# Import route modules
from app.routes import auth, products, orders, inventory, reviews, analytics, xml_api

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="A hybrid relational + NoSQL e-commerce backend demonstrating "
                "PostgreSQL, MongoDB, query optimization, partitioning, "
                "PL/pgSQL, triggers, aggregation pipelines, and XML support.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(inventory.router)
app.include_router(reviews.router)
app.include_router(analytics.router)
app.include_router(xml_api.router)


@app.on_event("startup")
def startup_event():
    """Initialize databases on server startup."""
    try:
        init_all()
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API status."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "databases": {
            "postgresql": "connected",
            "mongodb": "connected",
        },
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/auth",
            "products": "/api/products",
            "orders": "/api/orders",
            "inventory": "/api/inventory",
            "reviews": "/api/reviews",
            "analytics": "/api/analytics",
            "xml": "/api/xml",
        },
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    from sqlalchemy import text
    from app.db.postgres import engine
    from app.db.mongo import mongo_db

    pg_status = "ok"
    mongo_status = "ok"

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        pg_status = "error"

    try:
        mongo_db.command("ping")
    except Exception:
        mongo_status = "error"

    return {
        "status": "healthy" if pg_status == "ok" and mongo_status == "ok" else "degraded",
        "postgresql": pg_status,
        "mongodb": mongo_status,
    }

