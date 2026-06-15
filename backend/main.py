import os
import sys
import logging
from typing import List, Optional

# Ensure astroalgo_bot/ (the package folder) is on sys.path so config.py can be imported
# backend/main.py -> parent is astroalgo_bot, so add that directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Now import config from astroalgo_bot/config.py (or just config.py if in the same folder)
try:
    import config
except Exception:
    # Fallback: attempt to import as astroalgo_bot.config if package style is used
    try:
        from astroalgo_bot import config  # type: ignore
    except Exception as e:
        raise ImportError("Could not import config.py. Ensure astroalgo_bot/config.py exists.") from e

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Logging
LOG_LEVEL = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(level=LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger("astroalgo_bot")

# FastAPI app
app = FastAPI(
    title=getattr(config, "API_TITLE", "Astro Algo Bot API"),
    version=getattr(config, "API_VERSION", "1.0.0"),
    description=getattr(config, "API_DESCRIPTION", ""),
    docs_url="/docs" if getattr(config, "ENABLE_SWAGGER", True) else None,
    redoc_url="/redoc" if getattr(config, "ENABLE_REDOC", True) else None,
)

# CORS
allowed_origins: List[str] = getattr(config, "ALLOWED_ORIGINS", []) or []
# If ALLOWED_ORIGINS is empty, you may want to default to ["*"] in prod carefully
if not allowed_origins:
    logger.warning("ALLOWED_ORIGINS is empty; defaulting to ['*']. Update config.py to restrict origins.")
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=getattr(config, "ALLOW_CREDENTIALS", True),
    allow_methods=getattr(config, "ALLOW_METHODS", ["*"]),
    allow_headers=getattr(config, "ALLOW_HEADERS", ["*"]),
)

# Optional: serve static frontend (uncomment if you want to serve astroalgo.html)
# from fastapi.staticfiles import StaticFiles
# STATIC_DIR = os.path.join(ROOT_DIR)  # repo root - adjust if your html is elsewhere
# app.mount("/static", StaticFiles(directory= astroalgo.html at /static/astroalgo.html

# Error handler example
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Health check
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "environment": getattr(config, "ENVIRONMENT", "unknown")}

# Root
@app.get("/", tags=["root"])
async def root():
    return {"message": "Astro Algo Bot API is running", "version": getattr(config, "API_VERSION", "1.0.0")}

# Example API route (replace with your real endpoints / routers)
@app.get("/api/example", tags=["example"])
async def example(q: Optional[str] = None):
    return {"hello": "world", "q": q}