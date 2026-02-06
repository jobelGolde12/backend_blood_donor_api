from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class BloodType(str, enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RECENTLY_DONATED = "recently_donated"


class RegistrationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class DonorRegistration(Base):
    __tablename__ = "donor_registrations"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    contact_number = Column(String, nullable=False, index=True)
    email = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    municipality = Column(String, nullable=False)
    availability = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE, nullable=False)
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING, nullable=False)
    review_reason = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DonorProfile(Base):
    __tablename__ = "donor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    registration_id = Column(Integer, ForeignKey("donor_registrations.id"), nullable=False)
    age = Column(Integer, nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    municipality = Column(String, nullable=False)
    availability = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
