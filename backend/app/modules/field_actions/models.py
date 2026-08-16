from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from datetime import datetime, timezone
from app.core.database import Base

class ActionType(str):
    ACKNOWLEDGE = "ACKNOWLEDGE"
    IN_PROGRESS = "IN_PROGRESS"
    ON_SITE = "ON_SITE"
    ACTION_TAKEN = "ACTION_TAKEN"
    RESOLVED = "RESOLVED"
    REOPENED = "REOPENED"
    AWAITING_FEEDBACK = "AWAITING_FEEDBACK"
    CLOSED = "CLOSED"
    REOPEN_LIMIT_REACHED = "REOPEN_LIMIT_REACHED"

# State transition rules mapping (From -> Allowed To)
VALID_TRANSITIONS = {
    "SUBMITTED": [ActionType.ACKNOWLEDGE],
    ActionType.ACKNOWLEDGE: [ActionType.IN_PROGRESS, ActionType.RESOLVED],
    ActionType.IN_PROGRESS: [ActionType.ON_SITE, ActionType.ACTION_TAKEN, ActionType.RESOLVED],
    ActionType.ON_SITE: [ActionType.ACTION_TAKEN, ActionType.RESOLVED],
    ActionType.ACTION_TAKEN: [ActionType.RESOLVED],
    ActionType.RESOLVED: [ActionType.AWAITING_FEEDBACK],
    ActionType.AWAITING_FEEDBACK: [ActionType.CLOSED, ActionType.REOPENED, ActionType.REOPEN_LIMIT_REACHED],
    ActionType.REOPENED: [ActionType.IN_PROGRESS]
}

class FieldAction(Base):
    __tablename__ = "field_actions"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), index=True, nullable=False)
    officer_id = Column(String, ForeignKey("officers.id"), nullable=False)
    
    action_type = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
