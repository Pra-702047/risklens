from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.complaints.models import Complaint, ComplaintAIAnalysis
from app.modules.sla.models import SLAStatus, SLAState
from app.modules.field_actions.models import ActionType

def get_complaint_volume(db: Session) -> int:
    return db.query(func.count(Complaint.id)).scalar() or 0

def get_open_complaints(db: Session) -> int:
    return db.query(func.count(Complaint.id)).filter(
        Complaint.status.notin_([ActionType.RESOLVED, ActionType.AWAITING_FEEDBACK, ActionType.CLOSED, ActionType.REOPEN_LIMIT_REACHED])
    ).scalar() or 0

def get_critical_complaints(db: Session) -> int:
    return db.query(func.count(Complaint.id)).filter(
        Complaint.priority.in_(["P0", "P1"]),
        Complaint.status.notin_([ActionType.RESOLVED, ActionType.AWAITING_FEEDBACK, ActionType.CLOSED, ActionType.REOPEN_LIMIT_REACHED])
    ).scalar() or 0

def get_sla_risk_count(db: Session) -> int:
    return db.query(func.count(SLAStatus.id)).filter(
        SLAStatus.status == SLAState.WARNING
    ).scalar() or 0

def get_sla_breach_count(db: Session) -> int:
    return db.query(func.count(SLAStatus.id)).filter(
        SLAStatus.status == SLAState.BREACHED
    ).scalar() or 0

def get_ai_override_rate(db: Session) -> float:
    total_reviews = db.query(func.count(ComplaintAIAnalysis.id)).filter(
        ComplaintAIAnalysis.review_status.in_(["APPROVED", "REJECTED"])
    ).scalar() or 0
    
    if total_reviews == 0:
        return 0.0
        
    overridden = db.query(func.count(ComplaintAIAnalysis.id)).filter(
        ComplaintAIAnalysis.overridden == True
    ).scalar() or 0
    
    return (overridden / total_reviews) * 100

def get_low_confidence_rate(db: Session, threshold: float = 0.8) -> float:
    total = db.query(func.count(ComplaintAIAnalysis.id)).scalar() or 0
    if total == 0:
        return 0.0
        
    low_conf = db.query(func.count(ComplaintAIAnalysis.id)).filter(
        ComplaintAIAnalysis.confidence < threshold
    ).scalar() or 0
    
    return (low_conf / total) * 100

def get_department_performance(db: Session) -> dict:
    """Returns the count of open vs resolved complaints grouped by department."""
    # Count open complaints per department
    open_counts = db.query(
        Complaint.department_id, 
        func.count(Complaint.id)
    ).filter(
        Complaint.department_id.isnot(None),
        Complaint.status.notin_([ActionType.RESOLVED, ActionType.AWAITING_FEEDBACK, ActionType.CLOSED, ActionType.REOPEN_LIMIT_REACHED])
    ).group_by(Complaint.department_id).all()
    
    # Count resolved complaints per department
    resolved_counts = db.query(
        Complaint.department_id, 
        func.count(Complaint.id)
    ).filter(
        Complaint.department_id.isnot(None),
        Complaint.status.in_([ActionType.RESOLVED, ActionType.AWAITING_FEEDBACK, ActionType.CLOSED])
    ).group_by(Complaint.department_id).all()
    
    performance = {}
    for dept, count in open_counts:
        if dept not in performance:
            performance[dept] = {"open": 0, "resolved": 0}
        performance[dept]["open"] = count
        
    for dept, count in resolved_counts:
        if dept not in performance:
            performance[dept] = {"open": 0, "resolved": 0}
        performance[dept]["resolved"] = count
        
    return performance

def get_category_accuracy(db: Session) -> list:
    """Returns the accuracy rate for each AI predicted category."""
    # Count total predictions per category
    total_counts = db.query(
        ComplaintAIAnalysis.predicted_category,
        func.count(ComplaintAIAnalysis.id)
    ).group_by(ComplaintAIAnalysis.predicted_category).all()
    
    # Count overridden predictions per category
    overridden_counts = db.query(
        ComplaintAIAnalysis.predicted_category,
        func.count(ComplaintAIAnalysis.id)
    ).filter(
        ComplaintAIAnalysis.overridden == True
    ).group_by(ComplaintAIAnalysis.predicted_category).all()
    
    overridden_map = {cat: count for cat, count in overridden_counts}
    
    accuracy_list = []
    for cat, total in total_counts:
        if not cat: continue
        overridden = overridden_map.get(cat, 0)
        accuracy = ((total - overridden) / total) * 100 if total > 0 else 0
        accuracy_list.append({
            "category": cat,
            "accuracy": round(accuracy, 1)
        })
        
    return accuracy_list

