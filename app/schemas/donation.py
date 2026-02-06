from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class DonationCreate(BaseModel):
    donor_profile_id: int
    donation_date: date
    blood_type: str
    units: int = 1
    location: str


class DonationResponse(BaseModel):
    id: int
    donor_profile_id: int
    donation_date: date
    blood_type: str
    units: int
    location: str
    created_at: datetime

    class Config:
        from_attributes = True


class BloodRequestCreate(BaseModel):
    patient_name: str
    blood_type: str
    units_needed: int
    urgency: str = "medium"
    hospital: str
    contact_number: str


class BloodRequestResponse(BaseModel):
    id: int
    patient_name: str
    blood_type: str
    units_needed: int
    urgency: str
    hospital: str
    contact_number: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
