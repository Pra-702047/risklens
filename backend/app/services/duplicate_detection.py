from sqlalchemy.orm import Session
from app.modules.complaints.models import Complaint, ComplaintStatus
from app.modules.incidents.models import Incident, IncidentStatus
from app.services.haversine import HaversineGeoProvider
from app.utils.id_generator import generate_incident_id
from datetime import datetime, timezone, timedelta
import difflib

def calculate_text_similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def process_complaint_clustering(db: Session, new_complaint: Complaint) -> Incident:
    """
    Duplicate Detection:
    1. Find all active incidents within 500 meters of the same category.
    2. Check text similarity of descriptions to determine if it's the same incident.
    3. Link to existing Incident or create a new one.
    """
    
    # 1. Fetch active incidents of the same category
    active_incidents = db.query(Incident).filter(
        Incident.category == new_complaint.category,
        Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS])
    ).all()
    
    # 2. Filter by distance (500 meters)
    nearby_incidents = HaversineGeoProvider.filter_within_radius(
        new_complaint.latitude, new_complaint.longitude, active_incidents, radius_meters=500
    )
    
    best_match = None
    highest_similarity = 0.0
    
    # 3. Check similarity
    for incident, distance in nearby_incidents:
        # Fetch complaints under this incident to compare text
        existing_complaints = db.query(Complaint).filter(Complaint.incident_id == incident.id).all()
        for ec in existing_complaints:
            sim = calculate_text_similarity(new_complaint.description, ec.description)
            if sim > highest_similarity:
                highest_similarity = sim
                best_match = incident
                
    # 4. Link or Create
    # If we have a very similar description (>= 0.4) nearby, link it
    if best_match and highest_similarity >= 0.4:
        new_complaint.incident_id = best_match.id
        best_match.report_count += 1
        best_match.last_reported_at = datetime.now(timezone.utc)
        db.commit()
        return best_match
    
    # Create new Incident
    incident_id = generate_incident_id()
    new_incident = Incident(
        id=incident_id,
        incident_code=f"INC-{incident_id[:6].upper()}",
        category=new_complaint.category,
        latitude=new_complaint.latitude,
        longitude=new_complaint.longitude,
        status=IncidentStatus.OPEN,
        report_count=1
    )
    db.add(new_incident)
    new_complaint.incident_id = new_incident.id
    db.commit()
    db.refresh(new_incident)
    
    return new_incident
