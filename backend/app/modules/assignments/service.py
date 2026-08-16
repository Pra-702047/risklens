from sqlalchemy.orm import Session
from app.modules.assignments.models import Assignment, AssignmentStatus
from app.modules.users.models import Officer
from fastapi import HTTPException
from datetime import datetime, timezone
import uuid

def get_department_queue(db: Session, officer: Officer, filters: dict = None):
    """
    Returns complaints assigned to the officer's department.
    Future: Add support for filters (priority, category, etc).
    """
    from app.modules.complaints.models import Complaint
    query = db.query(Complaint).filter(Complaint.department_id == officer.department_id)
    
    # In a real implementation, we would apply filters here.
    return query.all()

def claim_complaint(db: Session, complaint_id: str, officer: Officer) -> Assignment:
    from app.modules.complaints.models import Complaint
    
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    if complaint.department_id != officer.department_id:
        raise HTTPException(status_code=403, detail="Cannot claim complaint from another department")
        
    # Check if already claimed by someone else
    existing_assignment = db.query(Assignment).filter(
        Assignment.complaint_id == complaint_id,
        Assignment.status == AssignmentStatus.CLAIMED
    ).first()
    
    if existing_assignment:
        if existing_assignment.officer_id == officer.id:
            return existing_assignment # Already claimed by this officer
        raise HTTPException(status_code=400, detail="Complaint already claimed by another officer")
        
    assignment = Assignment(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        department_id=complaint.department_id,
        officer_id=officer.id,
        status=AssignmentStatus.CLAIMED,
        claimed_at=datetime.now(timezone.utc)
    )
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
