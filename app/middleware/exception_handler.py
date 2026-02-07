from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class BloodDonorAPIException(Exception):
    """Custom exception for blood donor API."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


async def blood_donor_exception_handler(request: Request, exc: BloodDonorAPIException):
    """Handle custom blood donor API exceptions."""
    logger.error(f"BloodDonorAPIException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "type": "BloodDonorAPIException",
            "path": str(request.url.path),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "type": "HTTPException",
            "status_code": exc.status_code,
            "path": str(request.url.path),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions."""
    # Process errors to make them JSON serializable
    errors = []
    for error in exc.errors():
        processed_error = {}
        for key, value in error.items():
            if key == 'ctx' and isinstance(value, dict):
                # Handle the 'ctx' field which may contain non-serializable objects
                processed_ctx = {}
                for ctx_key, ctx_value in value.items():
                    if isinstance(ctx_value, Exception):
                        processed_ctx[ctx_key] = str(ctx_value)
                    else:
                        processed_ctx[ctx_key] = ctx_value
                processed_error[key] = processed_ctx
            elif isinstance(value, Exception):
                processed_error[key] = str(value)
            else:
                processed_error[key] = value
        errors.append(processed_error)

    logger.warning(f"Validation error: {errors}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation failed",
            "type": "ValidationError",
            "details": errors,
            "path": str(request.url.path),
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy exceptions."""
    logger.error(f"Database error: {str(exc)}")

    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=409,
            content={
                "error": True,
                "message": "Database integrity constraint violated",
                "type": "IntegrityError",
                "path": str(request.url.path),
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal database error",
            "type": "DatabaseError",
            "path": str(request.url.path),
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error" if not settings.debug else str(exc),
            "type": "InternalServerError",
            "path": str(request.url.path),
        },
    )


def setup_exception_handlers(app: FastAPI):
    """Setup all exception handlers for the application."""
    app.add_exception_handler(BloodDonorAPIException, blood_donor_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
