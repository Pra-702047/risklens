from sqlalchemy.orm import Session
from app.modules.routing.models import RoutingRule

def get_routing_for_complaint(db: Session, category: str, zone_id: str = None, issue_priority: str = None) -> str:
    """
    Deterministically find the department_id based on category, zone, and priority.
    """
    
    # 1. Try exact match: Category + Zone + Priority
    if zone_id and issue_priority:
        rule = db.query(RoutingRule).filter(
            RoutingRule.category == category,
            RoutingRule.zone_id == zone_id,
            RoutingRule.issue_priority == issue_priority,
            RoutingRule.is_active == True
        ).order_by(RoutingRule.evaluation_priority.desc()).first()
        if rule: return rule.department_id

    # 2. Try match: Category + Zone
    if zone_id:
        rule = db.query(RoutingRule).filter(
            RoutingRule.category == category,
            RoutingRule.zone_id == zone_id,
            RoutingRule.issue_priority.is_(None),
            RoutingRule.is_active == True
        ).order_by(RoutingRule.evaluation_priority.desc()).first()
        if rule: return rule.department_id
            
    # 3. Try match: Category only
    rule = db.query(RoutingRule).filter(
        RoutingRule.category == category,
        RoutingRule.zone_id.is_(None),
        RoutingRule.issue_priority.is_(None),
        RoutingRule.is_active == True
    ).order_by(RoutingRule.evaluation_priority.desc()).first()
    
    if rule: return rule.department_id
        
    # 3. Fallback routing rule
    fallback_rule = db.query(RoutingRule).filter(
        RoutingRule.category == "FALLBACK",
        RoutingRule.is_active == True
    ).first()
    
    if fallback_rule:
        return fallback_rule.department_id
        
    # Hardcoded safety fallback if DB is completely unconfigured
    return "DEPT_GENERAL_ADMIN"

from app.modules.users.models import Officer
from app.modules.assignments.models import Assignment, AssignmentStatus
import uuid

def auto_assign_officer(db: Session, complaint_id: str, department_id: str, zone_id: str = None) -> bool:
    """
    Attempts to automatically find an active officer and assign them to the complaint.
    Returns True if assigned, False otherwise.
    """
    query = db.query(Officer).filter(
        Officer.department_id == department_id,
        Officer.is_active == True
    )
    
    # Try to find an officer matching both department and zone
    if zone_id:
        # In Postgres ARRAY, we would use any(), but for MVP standard SQL we can fetch and filter
        officers = query.all()
        matched = [o for o in officers if o.zone_ids and zone_id in o.zone_ids]
        if matched:
            target_officer = matched[0]
        else:
            target_officer = officers[0] if officers else None
    else:
        target_officer = query.first()
        
    if target_officer:
        assignment = Assignment(
            id=str(uuid.uuid4()),
            complaint_id=complaint_id,
            department_id=department_id,
            officer_id=target_officer.id,
            status=AssignmentStatus.PENDING
        )
        db.add(assignment)
        
        # Also update the complaint status
        from app.modules.complaints.models import Complaint, ComplaintStatus
        from app.modules.complaints.service import log_status_change
        
        complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        if complaint:
            old_status = complaint.status
            complaint.status = ComplaintStatus.ASSIGNED.value
            
            # Log status change
            log_status_change(db, complaint_id, old_status, complaint.status, "SYSTEM", f"Auto-assigned to {target_officer.id}")
            db.commit()
        return True
        
    return False
