from sqlalchemy.orm import Session
from app.modules.sla.models import SLAPolicy
import uuid

def seed_sla_policies(db: Session):
    print("Seeding SLA Policies...")
    
    policies = [
        # P0: Critical / immediate public-safety risk
        {"priority": "P0", "resolution_time_hours": 4, "warning_time_hours": 1, "escalation_time_hours": 2},
        # P1: High-impact / urgent
        {"priority": "P1", "resolution_time_hours": 24, "warning_time_hours": 4, "escalation_time_hours": 12},
        # P2: Normal civic/traffic issue
        {"priority": "P2", "resolution_time_hours": 72, "warning_time_hours": 24, "escalation_time_hours": 48},
        # P3: Low severity
        {"priority": "P3", "resolution_time_hours": 168, "warning_time_hours": 48, "escalation_time_hours": 72},
    ]
    
    for p in policies:
        existing = db.query(SLAPolicy).filter(SLAPolicy.priority == p["priority"], SLAPolicy.is_active == True).first()
        if not existing:
            policy = SLAPolicy(
                id=str(uuid.uuid4()),
                priority=p["priority"],
                resolution_time_hours=p["resolution_time_hours"],
                warning_time_hours=p["warning_time_hours"],
                escalation_time_hours=p["escalation_time_hours"]
            )
            db.add(policy)
            
    db.commit()
    print("SLA Policies Seeded Successfully.")

if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    seed_sla_policies(db)
    db.close()
