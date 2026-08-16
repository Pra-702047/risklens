from sqlalchemy.orm import Session
from app.modules.audit.models import ComplaintEvent
import uuid
import json

def log_event(
    db: Session, 
    complaint_id: str, 
    event_type: str, 
    old_value: str = None, 
    new_value: str = None, 
    actor_id: str = "SYSTEM", 
    metadata: dict = None
) -> ComplaintEvent:
    
    event = ComplaintEvent(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        event_type=event_type,
        old_value=old_value,
        new_value=new_value,
        actor_id=actor_id,
        metadata_json=json.dumps(metadata) if metadata else None
    )
    db.add(event)
    
    # Send Notification
    try:
        from app.modules.complaints.models import Complaint
        from app.modules.notifications.service import dispatch_notification
        
        complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        if complaint:
            dispatch_notification(
                db=db,
                complaint_id=complaint_id,
                user_id=complaint.user_id,
                event_type=event_type,
                channel="PUSH", # Defaulting to PUSH for MVP
                template_key=f"TEMPLATE_{event_type}",
                recipient=complaint.user_id
            )
    except Exception as e:
        import logging
        logging.error(f"Failed to dispatch notification: {e}")
        
    db.commit()
    db.refresh(event)
    return event
