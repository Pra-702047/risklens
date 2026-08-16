from sqlalchemy import Column, String, DateTime, Text, Integer
from datetime import datetime, timezone
from app.core.database import Base

class ConfigAuditLog(Base):
    """
    Tracks changes to configuration tables (SLA Policies, Routing Rules, Categories).
    """
    __tablename__ = "config_audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    entity_type = Column(String, nullable=False, index=True) # e.g. SLA_POLICY, CATEGORY
    entity_id = Column(String, nullable=False, index=True)
    
    event_type = Column(String, nullable=False) # CREATED, UPDATED, DELETED
    
    old_value = Column(Text, nullable=True) # JSON
    new_value = Column(Text, nullable=True) # JSON
    
    changed_by = Column(String, nullable=False) # Admin ID
    reason = Column(String, nullable=True)
    
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
