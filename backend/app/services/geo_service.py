from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.geo.models import Zone, Ward
from app.modules.complaints.models import Complaint
from typing import Optional, Tuple, List
import math

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance in meters between two points on the earth."""
    R = 6371000  # Radius of earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_nearby_complaints(db: Session, longitude: float, latitude: float, radius_meters: float = 100) -> List[Complaint]:
    """
    MVP implementation using Python-side math since PostGIS is unavailable.
    Fetches recent unresolved complaints and filters them by distance.
    """
    # Fetch active complaints (In production with PostGIS, use ST_DWithin)
    recent_complaints = db.query(Complaint).filter(Complaint.status != "RESOLVED", Complaint.status != "CLOSED").all()
    
    nearby = []
    for c in recent_complaints:
        if c.latitude and c.longitude:
            dist = haversine(latitude, longitude, c.latitude, c.longitude)
            if dist <= radius_meters:
                nearby.append(c)
                
    return nearby

import json
import shapely.geometry
from shapely.geometry import Point, shape

def get_zone_and_ward_for_point(db: Session, longitude: float, latitude: float) -> Tuple[Optional[Zone], Optional[Ward]]:
    """
    Finds the Ward and Zone that contains the given latitude/longitude using Shapely.
    Expects the Ward's boundary column to contain a valid GeoJSON string.
    """
    point = Point(longitude, latitude)
    
    # Check all wards
    wards = db.query(Ward).all()
    matched_ward = None
    
    for ward in wards:
        if ward.boundary:
            try:
                # Parse GeoJSON boundary
                geom_dict = json.loads(ward.boundary)
                ward_polygon = shape(geom_dict)
                
                # Point in Polygon check
                if ward_polygon.contains(point):
                    matched_ward = ward
                    break
            except Exception as e:
                print(f"Error parsing boundary for ward {ward.id}: {e}")
                continue
                
    if matched_ward:
        zone = db.query(Zone).filter(Zone.id == matched_ward.zone_id).first()
        return zone, matched_ward
        
    # Check all zones if no ward matches
    zones = db.query(Zone).all()
    for zone in zones:
        if zone.boundary:
            try:
                geom_dict = json.loads(zone.boundary)
                zone_polygon = shape(geom_dict)
                if zone_polygon.contains(point):
                    return zone, None
            except Exception:
                continue
                
    # Ultimate fallback if completely outside all zones
    zone = db.query(Zone).first()
    return zone, None

def import_geojson(db: Session, geojson_path: str, entity_type: str):
    pass

