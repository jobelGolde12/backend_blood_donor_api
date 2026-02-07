from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db.dependencies import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User, UserRole
from app.models.donor import DonorRegistration, DonorProfile
from app.schemas.donor import (
    DonorRegistrationCreate,
    DonorRegistrationResponse,
    DonorRegistrationReview,
)

router = APIRouter()


@router.post("", response_model=DonorRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def create_registration(
    registration: DonorRegistrationCreate,
    db: Session = Depends(get_db),
):
    """Create donor registration (public endpoint)."""
    # Check for any existing PENDING registration with the same contact number
    existing_pending = db.query(DonorRegistration).filter(
        DonorRegistration.contact_number == registration.contact_number,
        DonorRegistration.status == "pending"
    ).first()

    if existing_pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration already pending for this contact number"
        )

    try:
        db_registration = DonorRegistration(**registration.model_dump())
        db.add(db_registration)
        db.commit()
        db.refresh(db_registration)
        return db_registration
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction on error
        # Check if this is a unique constraint violation
        if 'contact_number' in str(e.orig).lower() or 'unique constraint' in str(e.orig).lower():
            # Check if there's already a pending registration (double-check)
            existing_pending = db.query(DonorRegistration).filter(
                DonorRegistration.contact_number == registration.contact_number,
                DonorRegistration.status == "pending"
            ).first()
            
            if existing_pending:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Registration already pending for this contact number"
                )
            else:
                # This is a different constraint violation
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Contact number already registered with a different status"
                )
        else:
            # Re-raise other integrity errors to be handled by the global exception handler
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Database constraint violation: {str(e.orig)}"
            )
    except Exception as e:
        db.rollback()  # Rollback the transaction on error
        # Re-raise the exception to be handled by the global exception handler
        raise e


@router.get("", response_model=List[DonorRegistrationResponse])
async def list_registrations(
    status_filter: str = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """List all registrations (admin only)."""
    query = db.query(DonorRegistration)
    if status_filter:
        query = query.filter(DonorRegistration.status == status_filter)
    return query.order_by(DonorRegistration.created_at.desc()).all()


@router.patch("/{registration_id}", response_model=DonorRegistrationResponse)
async def review_registration(
    registration_id: int,
    review: DonorRegistrationReview,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Review registration (admin only)."""
    registration = db.query(DonorRegistration).filter(
        DonorRegistration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    if registration.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration already reviewed"
        )
    
    registration.status = review.status
    registration.review_reason = review.review_reason
    registration.reviewed_by = admin.id
    from datetime import datetime
    registration.reviewed_at = datetime.utcnow()
    
    if review.status == "approved":
        user = db.query(User).filter(User.contact_number == registration.contact_number).first()
        if not user:
            user = User(
                full_name=registration.full_name,
                contact_number=registration.contact_number,
                email=registration.email,
                role=UserRole.DONOR,
            )
            db.add(user)
            db.flush()
        
        profile = DonorProfile(
            user_id=user.id,
            registration_id=registration.id,
            age=registration.age,
            blood_type=registration.blood_type,
            municipality=registration.municipality,
            availability=registration.availability,
        )
        db.add(profile)
    
    db.commit()
    db.refresh(registration)
    return registration
