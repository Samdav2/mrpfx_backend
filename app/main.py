"""
MRPFX Backend - FastAPI Application

WordPress-compatible authentication backend with phpass and bcrypt password support.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.core.config import settings
from app.db.session import ini_db
from app.v1.api.auth import router as auth_router
from app.v1.api.crypto_payments import router as crypto_payment_router


# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting %s...", settings.APP_NAME)

    # Create uploads directory if it doesn't exist
    os.makedirs("wp-content/uploads", exist_ok=True)

    await ini_db()
    logger.info("Database tables created/verified")
    yield
    # Shutdown
    logger.info("Shutting down %s...", settings.APP_NAME)


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="WordPress-compatible authentication backend with support for imported user data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files
app.mount("/wp-content", StaticFiles(directory="wp-content"), name="wp-content")


# Register routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
from app.v1.api.wordpress import router as wordpress_router
app.include_router(wordpress_router, prefix=settings.API_V1_PREFIX)
from app.v1.api.admin import router as admin_router
app.include_router(admin_router, prefix=settings.API_V1_PREFIX)
app.include_router(crypto_payment_router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "name": settings.APP_NAME,
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
