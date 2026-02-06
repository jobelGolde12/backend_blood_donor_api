from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.dependencies import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.models.user import User
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_password_hash,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login using contact number."""
    user = db.query(User).filter(User.contact_number == request.contact_number).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active",
        )
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    user.hashed_refresh_token = get_password_hash(refresh_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    payload = verify_refresh_token(request.refresh_token, db)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user or not user.hashed_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    user.hashed_refresh_token = get_password_hash(refresh_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/logout")
async def logout(db: Session = Depends(get_db), user_id: int = Depends(lambda: 1)):
    """Logout by invalidating refresh token."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.hashed_refresh_token = None
        db.commit()
    
    return {"message": "Logged out successfully"}
