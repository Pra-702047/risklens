from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base

class AssignmentStatus(str):
    PENDING = "PENDING"
    CLAIMED = "CLAIMED"
    RELEASED = "RELEASED"

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), index=True, nullable=False)
    
    department_id = Column(String, nullable=False, index=True)
    team_id = Column(String, nullable=True)
    officer_id = Column(String, ForeignKey("officers.id"), nullable=True)
    
    status = Column(String, default=AssignmentStatus.PENDING, nullable=False)
    
    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    claimed_at = Column(DateTime(timezone=True), nullable=True)
    released_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
