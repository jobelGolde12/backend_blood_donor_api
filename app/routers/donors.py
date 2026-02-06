from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.db.dependencies import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.donor import DonorProfile
from app.schemas.donor_profile import DonorProfileResponse, DonorAvailabilityUpdate, DonorUpdate

router = APIRouter()


@router.get("", response_model=List[DonorProfileResponse])
async def list_donors(
    blood_type: Optional[str] = None,
    municipality: Optional[str] = None,
    availability: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List donors with filters and pagination."""
    query = db.query(
        DonorProfile,
        User.full_name,
        User.contact_number,
        User.email
    ).join(User, DonorProfile.user_id == User.id)
    
    if blood_type:
        query = query.filter(DonorProfile.blood_type == blood_type)
    if municipality:
        query = query.filter(DonorProfile.municipality == municipality)
    if availability:
        query = query.filter(DonorProfile.availability == availability)
    if search:
        query = query.filter(
            or_(
                User.full_name.ilike(f"%{search}%"),
                User.contact_number.ilike(f"%{search}%")
            )
        )
    
    results = query.offset(skip).limit(limit).all()
    
    return [
        DonorProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            full_name=full_name,
            contact_number=contact_number,
            email=email,
            age=profile.age,
            blood_type=profile.blood_type,
            municipality=profile.municipality,
            availability=profile.availability,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
        for profile, full_name, contact_number, email in results
    ]


@router.get("/{donor_id}", response_model=DonorProfileResponse)
async def get_donor(donor_id: int, db: Session = Depends(get_db)):
    """Get donor by ID."""
    result = db.query(
        DonorProfile,
        User.full_name,
        User.contact_number,
        User.email
    ).join(User, DonorProfile.user_id == User.id).filter(
        DonorProfile.id == donor_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    profile, full_name, contact_number, email = result
    return DonorProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        full_name=full_name,
        contact_number=contact_number,
        email=email,
        age=profile.age,
        blood_type=profile.blood_type,
        municipality=profile.municipality,
        availability=profile.availability,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


@router.patch("/{donor_id}", response_model=DonorProfileResponse)
async def update_donor(
    donor_id: int,
    update: DonorUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Update donor profile (admin only)."""
    profile = db.query(DonorProfile).filter(DonorProfile.id == donor_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    if update.age is not None:
        profile.age = update.age
    if update.municipality is not None:
        profile.municipality = update.municipality
    
    db.commit()
    return await get_donor(donor_id, db)


@router.patch("/{donor_id}/availability", response_model=DonorProfileResponse)
async def update_availability(
    donor_id: int,
    update: DonorAvailabilityUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Update donor availability (admin only)."""
    profile = db.query(DonorProfile).filter(DonorProfile.id == donor_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    profile.availability = update.availability
    db.commit()
    return await get_donor(donor_id, db)


@router.delete("/{donor_id}")
async def delete_donor(
    donor_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Soft delete donor (admin only)."""
    profile = db.query(DonorProfile).filter(DonorProfile.id == donor_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Donor not found")
    
    user = db.query(User).filter(User.id == profile.user_id).first()
    if user:
        user.status = "inactive"
    
    db.commit()
    return {"message": "Donor deleted successfully"}
