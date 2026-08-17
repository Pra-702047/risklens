from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.modules.users.models import Officer
from app.dependencies import get_current_officer
from app.modules.assignments.service import get_department_queue, claim_complaint
from app.modules.field_actions.service import log_field_action
from app.modules.complaints.models import Complaint

router = APIRouter(prefix="/officer/complaints", tags=["Officer Operations"])

@router.get("/")
def get_queue(
    priority: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_officer: Officer = Depends(get_current_officer)
):
    """
    Returns the department queue. Allows filtering by priority and status.
    """
    query = db.query(Complaint).filter(Complaint.department_id == current_officer.department_id)
    
    if priority:
        query = query.filter(Complaint.priority == priority)
    if status:
        query = query.filter(Complaint.status == status)
        
    return query.all()

@router.get("/{complaint_id}")
def get_complaint_details(
    complaint_id: str,
    db: Session = Depends(get_db),
    current_officer: Officer = Depends(get_current_officer)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id,
        Complaint.department_id == current_officer.department_id
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found or not in your department")
        
    return complaint

@router.post("/{complaint_id}/claim")
def claim(
    complaint_id: str,
    db: Session = Depends(get_db),
    current_officer: Officer = Depends(get_current_officer)
):
    assignment = claim_complaint(db, complaint_id, current_officer)
    return {"message": "Claim successful", "assignment_id": assignment.id}

@router.post("/{complaint_id}/actions")
def submit_field_action(
    complaint_id: str,
    action_type: str = Query(..., description="E.g., ACKNOWLEDGE, IN_PROGRESS, RESOLVED"),
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_officer: Officer = Depends(get_current_officer)
):
    print(f"DEBUG: submit_field_action called for {complaint_id} with {action_type} by officer {current_officer.id}")
    try:
        action = log_field_action(db, complaint_id, current_officer, action_type, notes)
        return {"message": "Field action logged", "action_id": action.id, "new_status": action_type}
    except Exception as e:
        print(f"DEBUG: log_field_action raised {repr(e)}")
        raise e
