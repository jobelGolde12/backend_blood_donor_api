from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class AlertType(str, enum.Enum):
    URGENT_REQUEST = "urgent_request"
    GENERAL_ANNOUNCEMENT = "general_announcement"
    DONATION_DRIVE = "donation_drive"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationType(str, enum.Enum):
    ALERT = "alert"
    MESSAGE_REPLY = "message_reply"
    SYSTEM = "system"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    target_audience = Column(JSON, nullable=True)
    send_now = Column(Boolean, default=True, nullable=False)
    schedule_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
