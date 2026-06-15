"""
Configuration template for Astro Algo Bot
"""
import os
from typing import Optional

# Environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# API Configuration
API_TITLE = "Astro Algo Bot API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "FastAPI backend for Astro Algo Bot trading system"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
WORKERS = int(os.getenv("WORKERS", 1))

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
ALLOW_CREDENTIALS = True
ALLOW_METHODS = ["*"]
ALLOW_HEADERS = ["*"]

# Database Configuration (if needed)
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)

# Trading Configuration
TRADING_ENABLED = os.getenv("TRADING_ENABLED", "False").lower() == "true"
METATRADER_HOST = os.getenv("METATRADER_HOST", "localhost")
METATRADER_PORT = int(os.getenv("METATRADER_PORT", 5555))

# API Keys and Secrets
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
API_KEY = os.getenv("API_KEY", None)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Feature Flags
ENABLE_SWAGGER = DEBUG or os.getenv("ENABLE_SWAGGER", "True").lower() == "true"
ENABLE_REDOC = DEBUG or os.getenv("ENABLE_REDOC", "True").lower() == "true"