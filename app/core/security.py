from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str, db: Session) -> Optional[Dict[str, Any]]:
    """Verify access token and return payload."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        # Check if it's an access token
        if payload.get("type") != "access":
            return None

        # Check if token has expired
        exp = payload.get("exp")
        if exp is None or datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        return payload
    except JWTError:
        return None


def verify_refresh_token(token: str, db: Session) -> Optional[Dict[str, Any]]:
    """Verify refresh token and return payload."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            return None

        # Check if token has expired
        exp = payload.get("exp")
        if exp is None or datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        return payload
    except JWTError:
        return None


def extract_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """Extract payload from token without verification (for debugging)."""
    try:
        # Decode without verification
        return jwt.decode(token, options={"verify_signature": False})
    except JWTError:
        return None
