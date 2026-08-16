from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text
from datetime import datetime, timezone
from app.core.database import Base

class ComplaintFeedback(Base):
    __tablename__ = "complaint_feedback"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False)
    
    rating = Column(Integer, nullable=False) # 1 to 5
    comment = Column(Text, nullable=True)
    resolution_accepted = Column(Boolean, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
