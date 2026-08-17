from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_role
from app.modules.incidents.models import Incident, IncidentStatus

router = APIRouter(prefix="/geo", tags=["geo"])

@router.get("/incidents")
def get_incidents_geojson(
    db: Session = Depends(get_db),
    # Optional: require authentication. The prompt says "GET /api/geo/incidents returning GeoJSON".
    # I'll let anyone authenticated view it, or maybe just officers/admins.
):
    incidents = db.query(Incident).filter(
        Incident.status.in_([IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS])
    ).all()
    
    features = []
    for inc in incidents:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [inc.longitude, inc.latitude]
            },
            "properties": {
                "id": inc.id,
                "incident_code": inc.incident_code,
                "category": inc.category,
                "status": inc.status,
                "report_count": inc.report_count
            }
        })
        
    return {
        "type": "FeatureCollection",
        "features": features
    }
