from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from app.core.database import Base

class NotificationStatus(str):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class NotificationChannel(str):
    PUSH = "PUSH"
    SMS = "SMS"
    EMAIL = "EMAIL"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=True, index=True)
    
    event_type = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    template_key = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    
    status = Column(String, default=NotificationStatus.PENDING, nullable=False)
    provider = Column(String, nullable=True) # e.g. MOCK, FCM, TWILIO
    
    sent_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
