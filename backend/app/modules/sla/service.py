from sqlalchemy.orm import Session
from app.modules.sla.models import SLAPolicy, SLAStatus, SLAState
from datetime import datetime, timezone, timedelta
import uuid

def calculate_and_assign_sla(db: Session, complaint_id: str, priority: str) -> SLAStatus:
    # Find active policy for this priority
    policy = db.query(SLAPolicy).filter(
        SLAPolicy.priority == priority,
        SLAPolicy.is_active == True
    ).first()
    
    if not policy:
        # Fallback to a default very long SLA if nothing is configured
        now = datetime.now(timezone.utc)
        status = SLAStatus(
            id=str(uuid.uuid4()),
            complaint_id=complaint_id,
            policy_id="FALLBACK_ID",
            status=SLAState.ON_TRACK,
            started_at=now,
            due_at=now + timedelta(hours=72),
            warning_at=now + timedelta(hours=48),
            escalate_at=now + timedelta(hours=96)
        )
        db.add(status)
        db.commit()
        db.refresh(status)
        return status
        
    now = datetime.now(timezone.utc)
    due_at = now + timedelta(hours=policy.resolution_time_hours)
    warning_at = due_at - timedelta(hours=policy.warning_time_hours)
    escalate_at = due_at + timedelta(hours=policy.escalation_time_hours)
    
    status = SLAStatus(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        policy_id=policy.id,
        status=SLAState.ON_TRACK,
        started_at=now,
        warning_at=warning_at,
        due_at=due_at,
        escalate_at=escalate_at
    )
    
    db.add(status)
    db.commit()
    db.refresh(status)
    return status
