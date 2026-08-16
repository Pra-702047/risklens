from sqlalchemy.orm import Session
from app.modules.geo.models import Zone
import uuid

def seed_zones(db: Session):
    print("Seeding Zones...")
    
    zones = [
        {"name": "Dharampeth Zone", "code": "Z01"},
        {"name": "Hanuman Nagar Zone", "code": "Z02"},
        {"name": "Dhantoli Zone", "code": "Z03"},
        {"name": "Nehru Nagar Zone", "code": "Z04"}
    ]
    
    for z in zones:
        existing = db.query(Zone).filter(Zone.code == z["code"]).first()
        if not existing:
            # We skip adding actual MULTIPOLYGON geometry here. 
            # In production, geo_service.import_geojson() should be used.
            zone = Zone(id=str(uuid.uuid4()), name=z["name"], code=z["code"])
            db.add(zone)
            
    db.commit()
    print("Zones Seeded Successfully.")

if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    seed_zones(db)
    db.close()
