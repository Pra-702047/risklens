from sqlalchemy.orm import Session
from app.modules.complaints.models import Complaint
from datetime import datetime, timedelta, timezone
from typing import List
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.services.haversine import HaversineGeoProvider

def get_geo_candidates(db: Session, longitude: float, latitude: float, hours_window: int) -> List[Complaint]:
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_window)
    
    # Get recent complaints
    recent_candidates = db.query(Complaint).filter(
        Complaint.created_at >= cutoff_time
    ).all()
    
    # Filter within 500m using Haversine
    nearby = HaversineGeoProvider.filter_within_radius(latitude, longitude, recent_candidates, radius_meters=500)
    
    # Return just the complaint objects, not the distance tuple
    return [candidate for candidate, dist in nearby]
