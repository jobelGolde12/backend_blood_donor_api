from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AlertCreate(BaseModel):
    title: str
    message: str
    alert_type: str
    priority: str = "medium"
    target_audience: Optional[Dict[str, Any]] = None
    send_now: bool = True
    schedule_at: Optional[datetime] = None


class AlertResponse(BaseModel):
    id: int
    title: str
    message: str
    alert_type: str
    priority: str
    target_audience: Optional[Dict[str, Any]]
    send_now: bool
    schedule_at: Optional[datetime]
    sent_at: Optional[datetime]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    alert_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True
