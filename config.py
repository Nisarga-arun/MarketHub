"""
Application configuration.
Uses environment variables for flexible deployment.
"""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Uploads (product images)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "products")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB

    # Database
    MYSQL_USER = os.environ.get("MYSQL_USER", "25EMRITCS059")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "#2KDLKwHsX2OZObU")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "157.173.221.22")
    MYSQL_PORT = os.environ.get("MYSQL_PORT", "3308")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "25EMRITCS059")

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("SQLALCHEMY_DATABASE_URI")
        or (
            f"mysql+pymysql://{quote_plus(MYSQL_USER)}:{quote_plus(MYSQL_PASSWORD)}"
            f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
