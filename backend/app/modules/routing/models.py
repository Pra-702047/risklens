from sqlalchemy import Column, String, Boolean, Integer, DateTime
from datetime import datetime, timezone
from app.core.database import Base

class RoutingRule(Base):
    __tablename__ = "routing_rules"
    
    id = Column(String, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    zone_id = Column(String, nullable=True) # If null, applies to all zones
    issue_priority = Column(String, nullable=True) # e.g. P0. If null, applies to all priorities
    department_id = Column(String, nullable=False)
    team_id = Column(String, nullable=True)
    evaluation_priority = Column(Integer, default=0) # Changed from priority to evaluation_priority to avoid confusion
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
