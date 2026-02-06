from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.dependencies import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.models.donor import DonorProfile
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter()


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create message (donor to admin)."""
    profile = db.query(DonorProfile).filter(
        DonorProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only donors can send messages"
        )
    
    db_message = Message(
        donor_profile_id=profile.id,
        subject=message.subject,
        content=message.content,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("", response_model=List[MessageResponse])
async def list_messages(
    is_closed: bool = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """List all messages (admin only)."""
    query = db.query(Message)
    if is_closed is not None:
        query = query.filter(Message.is_closed == is_closed)
    return query.order_by(Message.created_at.desc()).all()


@router.patch("/{message_id}/close", response_model=MessageResponse)
async def close_message(
    message_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Close message (admin only)."""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_closed = True
    db.commit()
    db.refresh(message)
    return message
