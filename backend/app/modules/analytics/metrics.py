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
