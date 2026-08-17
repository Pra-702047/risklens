from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user, require_role
from app.modules.analytics import metrics
from app.modules.complaints.models import Complaint

router = APIRouter(prefix="/admin/analytics", tags=["Admin Analytics"])

@router.get("/overview")
def get_overview(db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN", "DEPARTMENT_ADMIN", "SUPERVISOR"]))):
    return {
        "open_complaints": metrics.get_open_complaints(db),
        "critical_complaints": metrics.get_critical_complaints(db),
        "sla_risk": metrics.get_sla_risk_count(db),
        "sla_breached": metrics.get_sla_breach_count(db),
        "total_volume": metrics.get_complaint_volume(db),
        "department_performance": metrics.get_department_performance(db)
    }

@router.get("/ai")
def get_ai_monitoring(db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN", "SUPERVISOR"]))):
    return {
        "override_rate": metrics.get_ai_override_rate(db),
        "low_confidence_rate": metrics.get_low_confidence_rate(db, 0.8),
        "category_accuracy": metrics.get_category_accuracy(db)
    }

@router.get("/map/active")
def get_active_map_data(db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN", "DEPARTMENT_ADMIN", "SUPERVISOR", "OFFICER"]))):
    from app.modules.field_actions.models import ActionType
    
    complaints = db.query(Complaint).filter(
        Complaint.status.notin_([ActionType.RESOLVED, ActionType.AWAITING_FEEDBACK, ActionType.CLOSED, ActionType.REOPEN_LIMIT_REACHED]),
        Complaint.latitude.isnot(None),
        Complaint.longitude.isnot(None)
    ).all()
    
    # Return as GeoJSON FeatureCollection
    features = []
    for c in complaints:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [c.longitude, c.latitude] # GeoJSON is [lon, lat]
            },
            "properties": {
                "id": c.id,
                "category": c.category,
                "priority": c.priority or "P3",
                "status": c.status
            }
        })
        
    return {
        "type": "FeatureCollection",
        "features": features
    }
