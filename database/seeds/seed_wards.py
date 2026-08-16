from sqlalchemy.orm import Session
from app.modules.geo.models import Zone, Ward
import uuid

def seed_wards(db: Session):
    print("Seeding Wards...")
    
    dharampeth = db.query(Zone).filter(Zone.code == "Z01").first()
    
    if not dharampeth:
        print("Zone Z01 not found. Run seed_zones.py first.")
        return
        
    wards = [
        {"name": "Gokulpeth", "code": "W01-A", "zone_id": dharampeth.id},
        {"name": "Civil Lines", "code": "W01-B", "zone_id": dharampeth.id},
    ]
    
    for w in wards:
        existing = db.query(Ward).filter(Ward.code == w["code"]).first()
        if not existing:
            ward = Ward(id=str(uuid.uuid4()), name=w["name"], code=w["code"], zone_id=w["zone_id"])
            db.add(ward)
            
    db.commit()
    print("Wards Seeded Successfully.")

if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    seed_wards(db)
    db.close()
