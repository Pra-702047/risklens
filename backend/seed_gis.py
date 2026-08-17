import json
import uuid
import sys
import os

from app.core.database import SessionLocal
from app.modules.geo.models import Zone, Ward

def seed_gis():
    db = SessionLocal()
    
    # 1. Clear existing Wards and Zones
    db.query(Ward).delete()
    db.query(Zone).delete()
    db.commit()
    
    # Define a Zone that covers roughly New Delhi center
    # Longitude ~ 77.2, Latitude ~ 28.6
    
    # Zone: North Delhi
    zone_id = str(uuid.uuid4())
    zone_polygon = {
        "type": "Polygon",
        "coordinates": [[
            [77.0, 28.5], 
            [77.4, 28.5], 
            [77.4, 28.9], 
            [77.0, 28.9], 
            [77.0, 28.5]
        ]]
    }
    
    zone = Zone(
        id=zone_id,
        name="North Delhi Zone",
        code="NDZ-01",
        boundary=json.dumps(zone_polygon)
    )
    db.add(zone)
    
    # Ward: Model Town (Inside North Delhi Zone)
    ward1_id = str(uuid.uuid4())
    ward1_polygon = {
        "type": "Polygon",
        "coordinates": [[
            [77.15, 28.65], 
            [77.25, 28.65], 
            [77.25, 28.75], 
            [77.15, 28.75], 
            [77.15, 28.65]
        ]]
    }
    
    ward1 = Ward(
        id=ward1_id,
        name="Model Town Ward",
        code="MTW-01",
        zone_id=zone_id,
        boundary=json.dumps(ward1_polygon)
    )
    db.add(ward1)
    
    db.commit()
    print("GIS seeding completed successfully!")
    db.close()

if __name__ == "__main__":
    seed_gis()
