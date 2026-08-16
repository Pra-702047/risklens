from sqlalchemy.orm import Session
from app.modules.severity.models import ComplaintSeverity
from ai.severity_scoring.scorer import assess_severity
import uuid
import json

def generate_and_save_severity(db: Session, complaint_id: str, category: str, description: str, address: str) -> ComplaintSeverity:
    result = assess_severity(category, description, address or "")
    
    severity_record = ComplaintSeverity(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        priority=result["priority"],
        severity_score=result["severity_score"],
        severity_reasons=json.dumps(result["severity_reasons"]),
        model_provider=result["model_provider"],
        model_name=result["model_name"]
    )
    
    db.add(severity_record)
    db.commit()
    db.refresh(severity_record)
    return severity_record
