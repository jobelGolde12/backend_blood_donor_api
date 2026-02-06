from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.dependencies import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.donor import DonorProfile
from app.models.donation import Donation, BloodRequest
from app.schemas.donation import (
    DonationCreate,
    DonationResponse,
    BloodRequestCreate,
    BloodRequestResponse,
)

router = APIRouter()


@router.get("/donations", response_model=List[DonationResponse])
async def list_donations(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    blood_type: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """List donations with filters."""
    query = db.query(Donation)
    
    if start_date:
        query = query.filter(Donation.donation_date >= start_date)
    if end_date:
        query = query.filter(Donation.donation_date <= end_date)
    if blood_type:
        query = query.filter(Donation.blood_type == blood_type)
    
    return query.order_by(Donation.donation_date.desc()).all()


@router.post("/donations", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Create donation record and update donor availability."""
    profile = db.query(DonorProfile).filter(
        DonorProfile.id == donation.donor_profile_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Donor profile not found")
    
    db_donation = Donation(**donation.model_dump())
    db.add(db_donation)
    
    profile.availability = "recently_donated"
    
    db.commit()
    db.refresh(db_donation)
    return db_donation


@router.get("/requests", response_model=List[BloodRequestResponse])
async def list_requests(
    blood_type: Optional[str] = None,
    urgency: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List blood requests with filters."""
    query = db.query(BloodRequest)
    
    if blood_type:
        query = query.filter(BloodRequest.blood_type == blood_type)
    if urgency:
        query = query.filter(BloodRequest.urgency == urgency)
    
    return query.order_by(BloodRequest.created_at.desc()).all()


@router.post("/requests", response_model=BloodRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request: BloodRequestCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Create blood request."""
    db_request = BloodRequest(
        **request.model_dump(),
        created_by=admin.id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
