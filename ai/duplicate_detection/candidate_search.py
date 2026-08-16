from sqlalchemy.orm import Session
from app.modules.complaints.models import Complaint
from datetime import datetime, timedelta
from typing import List

def get_geo_candidates(db: Session, longitude: float, latitude: float, hours_window: int) -> List[Complaint]:
    """
    Mocked for MVP without PostGIS.
    Returns complaints within the time window, ignoring geography to avoid PostGIS requirement.
    """
    cutoff_time = datetime.utcnow() - timedelta(hours=hours_window)
    
    candidates = db.query(Complaint).filter(
        Complaint.created_at >= cutoff_time
    ).all()
    
    return candidates
