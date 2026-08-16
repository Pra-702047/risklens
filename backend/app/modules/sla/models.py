from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base

class SLAState(str):
    ON_TRACK = "ON_TRACK"
    WARNING = "WARNING"
    BREACHED = "BREACHED"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"

class SLAPolicy(Base):
    __tablename__ = "sla_policies"
    
    id = Column(String, primary_key=True, index=True)
    priority = Column(String, index=True, nullable=False) # e.g. P0, P1
    
    resolution_time_hours = Column(Integer, nullable=False)
    warning_time_hours = Column(Integer, nullable=False) # Time before resolution to warn
    escalation_time_hours = Column(Integer, nullable=False) # Time after resolution to escalate
    
    is_active = Column(Boolean, default=True)
    effective_from = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    effective_until = Column(DateTime(timezone=True), nullable=True)

class SLAStatus(Base):
    __tablename__ = "sla_status"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), unique=True, index=True, nullable=False)
    policy_id = Column(String, ForeignKey("sla_policies.id"), nullable=False)
    
    status = Column(String, default=SLAState.ON_TRACK, nullable=False)
    
    # Computed Deadlines
    started_at = Column(DateTime(timezone=True), nullable=False)
    warning_at = Column(DateTime(timezone=True), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)
    escalate_at = Column(DateTime(timezone=True), nullable=False)
    
    # Actual occurrences
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    breached_at = Column(DateTime(timezone=True), nullable=True)
    escalated_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
