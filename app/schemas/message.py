from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    subject: str
    content: str


class MessageResponse(BaseModel):
    id: int
    donor_profile_id: int
    subject: str
    content: str
    is_closed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
