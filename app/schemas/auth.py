from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class LoginRequest(BaseModel):
    contact_number: str = Field(..., description="Philippine mobile number")
    
    @field_validator("contact_number")
    @classmethod
    def validate_ph_number(cls, v: str) -> str:
        pattern = r"^(09|\+639)\d{9}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid Philippine mobile number format")
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None
