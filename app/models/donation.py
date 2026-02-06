from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
import enum

from app.db.session import Base
from app.models.donor import BloodType


class UrgencyLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_profile_id = Column(Integer, ForeignKey("donor_profiles.id"), nullable=False)
    donation_date = Column(Date, nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    units = Column(Integer, default=1, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    units_needed = Column(Integer, nullable=False)
    urgency = Column(Enum(UrgencyLevel), default=UrgencyLevel.MEDIUM, nullable=False)
    hospital = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
