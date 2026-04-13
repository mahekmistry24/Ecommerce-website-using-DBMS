"""
Application configuration loaded from .env file.
"""
import os
from dotenv import load_dotenv

# Load .env from the backend directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


class Settings:
    # PostgreSQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:mahek-adbms@localhost:5432/adbms_ecommerce"
    )

    # MongoDB
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "adbms_ecommerce")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "adbms-ecommerce-super-secret-key-2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # App
    APP_NAME: str = os.getenv("APP_NAME", "Smart Distributed E-Commerce System")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()
