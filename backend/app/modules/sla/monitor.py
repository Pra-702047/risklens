from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import SessionLocal
from app.modules.sla.models import SLAStatus, SLAState
from app.modules.complaints.models import Complaint
from app.modules.field_actions.models import ActionType

def check_sla_breaches():
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        
        # We only check SLAs for complaints that are NOT resolved or closed
        active_slas = db.query(SLAStatus).join(Complaint).filter(
            SLAStatus.status.notin_([SLAState.RESOLVED]),
            Complaint.status.notin_([ActionType.RESOLVED, ActionType.AWAITING_FEEDBACK, ActionType.CLOSED, ActionType.REOPEN_LIMIT_REACHED])
        ).all()
        
        for sla in active_slas:
            # Check for Escalation
            if sla.status != SLAState.ESCALATED and now >= sla.escalate_at:
                sla.status = SLAState.ESCALATED
                sla.escalated_at = now
                db.commit()
                # Optionally trigger notification here
                continue
                
            # Check for Breach
            if sla.status not in [SLAState.BREACHED, SLAState.ESCALATED] and now >= sla.due_at:
                sla.status = SLAState.BREACHED
                sla.breached_at = now
                db.commit()
                # Optionally trigger notification here
                continue
                
            # Check for Warning
            if sla.status == SLAState.ON_TRACK and now >= sla.warning_at:
                sla.status = SLAState.WARNING
                db.commit()
                
    except Exception as e:
        print(f"Error checking SLAs: {e}")
    finally:
        db.close()
