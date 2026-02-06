from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import date

from app.db.dependencies import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.donor import DonorProfile
from app.models.donation import Donation

router = APIRouter()


@router.get("/summary")
async def get_summary(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Get summary statistics."""
    total_donors = db.query(func.count(DonorProfile.id)).scalar()
    available_donors = db.query(func.count(DonorProfile.id)).filter(
        DonorProfile.availability == "available"
    ).scalar()
    total_donations = db.query(func.count(Donation.id)).scalar()
    
    return {
        "total_donors": total_donors,
        "available_donors": available_donors,
        "total_donations": total_donations,
    }


@router.get("/blood-type-distribution")
async def get_blood_type_distribution(
    municipality: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Get blood type distribution."""
    query = db.query(
        DonorProfile.blood_type,
        func.count(DonorProfile.id).label("count")
    )
    
    if municipality:
        query = query.filter(DonorProfile.municipality == municipality)
    
    results = query.group_by(DonorProfile.blood_type).all()
    
    return {
        "distribution": [
            {"blood_type": blood_type, "count": count}
            for blood_type, count in results
        ]
    }


@router.get("/monthly-donations")
async def get_monthly_donations(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Get monthly donation statistics."""
    query = db.query(
        extract("year", Donation.donation_date).label("year"),
        extract("month", Donation.donation_date).label("month"),
        func.count(Donation.id).label("count"),
        func.sum(Donation.units).label("total_units")
    )
    
    if start_date:
        query = query.filter(Donation.donation_date >= start_date)
    if end_date:
        query = query.filter(Donation.donation_date <= end_date)
    
    results = query.group_by("year", "month").order_by("year", "month").all()
    
    return {
        "monthly_data": [
            {
                "year": int(year),
                "month": int(month),
                "donation_count": count,
                "total_units": total_units or 0
            }
            for year, month, count, total_units in results
        ]
    }


@router.get("/availability-trend")
async def get_availability_trend(
    municipality: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Get donor availability trend."""
    query = db.query(
        DonorProfile.availability,
        func.count(DonorProfile.id).label("count")
    )
    
    if municipality:
        query = query.filter(DonorProfile.municipality == municipality)
    
    results = query.group_by(DonorProfile.availability).all()
    
    return {
        "availability": [
            {"status": availability, "count": count}
            for availability, count in results
        ]
    }
