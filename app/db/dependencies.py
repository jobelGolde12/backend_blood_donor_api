from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import verify_token, verify_refresh_token


# Database dependency
def get_current_db(db: Session = Depends(get_db)) -> Session:
    """Get current database session."""
    return db


# Authentication dependencies
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Get current authenticated user."""
    token = credentials.credentials
    payload = verify_token(token, db)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def get_current_active_user(current_user=Depends(get_current_user)):
    """Get current active user."""
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_current_admin_user(current_user=Depends(get_current_active_user)):
    """Get current admin user."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


def get_current_donor_user(current_user=Depends(get_current_active_user)):
    """Get current donor user."""
    if current_user.get("role") != "donor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


def verify_refresh_token_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Verify refresh token for token refresh endpoint."""
    token = credentials.credentials
    payload = verify_refresh_token(token, db)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
