from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    full_name: str
    contact_number: str
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    role: str
    status: str
    theme_preference: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("contact_number")
    @classmethod
    def validate_ph_number(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        pattern = r"^(09|\+639)\d{9}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid Philippine mobile number format")
        return v


class PreferenceUpdate(BaseModel):
    theme_preference: str

    @field_validator("theme_preference")
    @classmethod
    def validate_theme(cls, v: str) -> str:
        if v not in ["light", "dark", "system"]:
            raise ValueError("Theme must be light, dark, or system")
        return v
