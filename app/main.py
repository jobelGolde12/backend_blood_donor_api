from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.exception_handler import setup_exception_handlers

limiter = Limiter(key_func=get_remote_address)


def create_app() -> FastAPI:
    """Create FastAPI application with all configurations."""

    # Setup logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Add rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add trusted host middleware for production
    if settings.environment == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"],  # Configure appropriately for production
        )

    # Setup exception handlers
    setup_exception_handlers(app)

    # Include routers
    from app.routers import auth, users, donors, messages, alerts, notifications
    from app.routers import donations, reports, donor_registrations

    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(
        donor_registrations.router,
        prefix="/api/v1/donor-registrations",
        tags=["donor-registrations"],
    )
    app.include_router(donors.router, prefix="/api/v1/donors", tags=["donors"])
    app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
    app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
    app.include_router(
        notifications.router, prefix="/api/v1/notifications", tags=["notifications"]
    )
    app.include_router(donations.router, prefix="/api/v1/donations", tags=["donations"])
    app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.app_version}

    return app


# Create app instance
app = create_app()
