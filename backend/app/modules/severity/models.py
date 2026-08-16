from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from datetime import datetime, timezone
from app.core.database import Base

import enum

class PriorityEnum(str, enum.Enum):
    P0 = "P0" # Critical / immediate public-safety risk
    P1 = "P1" # High-impact / urgent
    P2 = "P2" # Normal civic/traffic issue
    P3 = "P3" # Low severity

class ComplaintSeverity(Base):
    __tablename__ = "complaint_severities"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), index=True, nullable=False)
    
    priority = Column(String, nullable=False)
    severity_score = Column(Integer, nullable=False) # 0-100
    severity_reasons = Column(Text, nullable=True) # JSON list of strings
    
    model_provider = Column(String, nullable=True)
    model_name = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
