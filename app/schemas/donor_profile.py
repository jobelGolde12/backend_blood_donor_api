from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DonorProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    contact_number: str
    email: Optional[str]
    age: int
    blood_type: str
    municipality: str
    availability: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class DonorAvailabilityUpdate(BaseModel):
    availability: str


class DonorUpdate(BaseModel):
    age: Optional[int] = None
    municipality: Optional[str] = None
