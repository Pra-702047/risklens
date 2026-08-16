from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from datetime import datetime, timezone
from app.core.database import Base

class EventType(str):
    COMPLAINT_CREATED = "COMPLAINT_CREATED"
    PRIORITY_ASSIGNED = "PRIORITY_ASSIGNED"
    ROUTE_ASSIGNED = "ROUTE_ASSIGNED"
    SLA_STARTED = "SLA_STARTED"
    SLA_WARNING = "SLA_WARNING"
    SLA_BREACHED = "SLA_BREACHED"
    SLA_ESCALATED = "SLA_ESCALATED"
    COMPLAINT_RESOLVED = "COMPLAINT_RESOLVED"

class ComplaintEvent(Base):
    __tablename__ = "complaint_events"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), index=True, nullable=False)
    event_type = Column(String, nullable=False, index=True)
    
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    
    actor_id = Column(String, nullable=True) # e.g. 'SYSTEM', 'AI', or user_id
    metadata_json = Column(Text, nullable=True) # JSON details
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
