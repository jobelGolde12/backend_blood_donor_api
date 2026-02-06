from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re


class DonorRegistrationCreate(BaseModel):
    full_name: str
    contact_number: str
    email: Optional[EmailStr] = None
    age: int
    blood_type: str
    municipality: str
    availability: str = "available"

    @field_validator("contact_number")
    @classmethod
    def validate_ph_number(cls, v: str) -> str:
        pattern = r"^(09|\+639)\d{9}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid Philippine mobile number format")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v

    @field_validator("blood_type")
    @classmethod
    def validate_blood_type(cls, v: str) -> str:
        valid = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if v not in valid:
            raise ValueError(f"Blood type must be one of {valid}")
        return v

    @field_validator("availability")
    @classmethod
    def validate_availability(cls, v: str) -> str:
        valid = ["available", "unavailable", "recently_donated"]
        if v not in valid:
            raise ValueError(f"Availability must be one of {valid}")
        return v


class DonorRegistrationResponse(BaseModel):
    id: int
    full_name: str
    contact_number: str
    email: Optional[str]
    age: int
    blood_type: str
    municipality: str
    availability: str
    status: str
    review_reason: Optional[str]
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class DonorRegistrationReview(BaseModel):
    status: str
    review_reason: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ["approved", "rejected"]:
            raise ValueError("Status must be approved or rejected")
        return v
