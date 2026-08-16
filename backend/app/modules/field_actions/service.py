from sqlalchemy.orm import Session
from app.modules.field_actions.models import FieldAction, VALID_TRANSITIONS, ActionType
from app.modules.assignments.models import Assignment, AssignmentStatus
from app.modules.users.models import Officer
from app.modules.audit.service import log_event
from fastapi import HTTPException
import uuid

def log_field_action(db: Session, complaint_id: str, officer: Officer, action_type: str, notes: str = None) -> FieldAction:
    from app.modules.complaints.models import Complaint
    
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    # Verify assignment ownership
    assignment = db.query(Assignment).filter(
        Assignment.complaint_id == complaint_id,
        Assignment.status == AssignmentStatus.CLAIMED
    ).first()
    
    if not assignment or assignment.officer_id != officer.id:
        raise HTTPException(status_code=403, detail="Must claim complaint before taking field action")
        
    # Verify State Transition
    current_state = complaint.status
    allowed_transitions = VALID_TRANSITIONS.get(current_state, [])
    
    if action_type not in allowed_transitions:
        raise HTTPException(status_code=400, detail=f"Invalid state transition from {current_state} to {action_type}")
        
    # Log the action
    action = FieldAction(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        officer_id=officer.id,
        action_type=action_type,
        notes=notes
    )
    db.add(action)
    
    # Update complaint state
    old_status = complaint.status
    complaint.status = action_type
    db.commit()
    db.refresh(action)
    
    # Audit trail
    log_event(db, complaint_id, action_type, old_value=old_status, new_value=action_type, actor_id=officer.id)
    
    return action
