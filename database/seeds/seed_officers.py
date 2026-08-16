from sqlalchemy.orm import Session
from app.modules.users.models import Officer, RoleEnum
import uuid

def seed_officers(db: Session):
    print("Seeding Officers...")
    
    officers = [
        {
            "firebase_uid": "OFFICER_PWD_01",
            "name": "Rajesh Kumar (PWD)",
            "email": "rajesh.pwd@risklens.local",
            "role": RoleEnum.OFFICER,
            "department_id": "DEPT_PWD",
            "zone_ids": ["Z01"]
        },
        {
            "firebase_uid": "OFFICER_TRAFFIC_01",
            "name": "Amit Singh (Traffic)",
            "email": "amit.traffic@risklens.local",
            "role": RoleEnum.OFFICER,
            "department_id": "DEPT_TRAFFIC",
            "zone_ids": ["Z01", "Z02"]
        }
    ]
    
    for o in officers:
        existing = db.query(Officer).filter(Officer.email == o["email"]).first()
        if not existing:
            officer = Officer(
                id=str(uuid.uuid4()),
                firebase_uid=o["firebase_uid"],
                name=o["name"],
                email=o["email"],
                role=o["role"],
                department_id=o["department_id"],
                zone_ids=o["zone_ids"]
            )
            db.add(officer)
            
    db.commit()
    print("Officers Seeded Successfully.")

if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    seed_officers(db)
    db.close()
