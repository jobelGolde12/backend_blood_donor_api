from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.dependencies import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.donor import DonorProfile
from app.models.notification import Alert, Notification
from app.schemas.notification import AlertCreate, AlertResponse

router = APIRouter()


def fan_out_notifications(db: Session, alert: Alert):
    """Create notifications for matching donors."""
    query = db.query(DonorProfile)
    
    if alert.target_audience:
        if "blood_type" in alert.target_audience:
            query = query.filter(DonorProfile.blood_type == alert.target_audience["blood_type"])
        if "municipality" in alert.target_audience:
            query = query.filter(DonorProfile.municipality == alert.target_audience["municipality"])
        if "availability" in alert.target_audience:
            query = query.filter(DonorProfile.availability == alert.target_audience["availability"])
    
    profiles = query.all()
    
    for profile in profiles:
        notification = Notification(
            user_id=profile.user_id,
            title=alert.title,
            message=alert.message,
            notification_type="alert",
            alert_id=alert.id,
        )
        db.add(notification)


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Create alert and optionally send notifications."""
    db_alert = Alert(
        title=alert.title,
        message=alert.message,
        alert_type=alert.alert_type,
        priority=alert.priority,
        target_audience=alert.target_audience,
        send_now=alert.send_now,
        schedule_at=alert.schedule_at,
        created_by=admin.id,
    )
    
    if alert.send_now:
        db_alert.sent_at = datetime.utcnow()
        db.add(db_alert)
        db.flush()
        fan_out_notifications(db, db_alert)
    else:
        db.add(db_alert)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    db: Session = Depends(get_db),
):
    """List all alerts (public)."""
    return db.query(Alert).order_by(Alert.created_at.desc()).all()


@router.post("/{alert_id}/send", response_model=AlertResponse)
async def send_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """Send scheduled alert."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    if alert.sent_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert already sent"
        )
    
    alert.sent_at = datetime.utcnow()
    fan_out_notifications(db, alert)
    db.commit()
    db.refresh(alert)
    return alert
