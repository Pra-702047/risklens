import sys
import os

# Ensure backend directory is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.core.database import SessionLocal, Base, engine
from app.modules.users.models import User, Officer, RoleEnum
from app.modules.routing.models import Department
from app.core.security import get_password_hash
import uuid

def seed_demo():
    print("Starting Demo Data Seeding...")
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Seed Departments
        dept_traffic = db.query(Department).filter(Department.id == "TRAFFIC_NMC").first()
        if not dept_traffic:
            dept_traffic = Department(id="TRAFFIC_NMC", name="Nagpur Traffic Police")
            db.add(dept_traffic)
            print("Seeded Department: Traffic")
            
        dept_roads = db.query(Department).filter(Department.id == "ROADS_NMC").first()
        if not dept_roads:
            dept_roads = Department(id="ROADS_NMC", name="NMC Road Department")
            db.add(dept_roads)
            print("Seeded Department: Roads")

        db.commit()

        # Seed Demo Citizen
        demo_citizen = db.query(User).filter(User.email == "demo@risklens.local").first()
        if not demo_citizen:
            demo_citizen = User(
                id=str(uuid.uuid4()),
                email="demo@risklens.local",
                password_hash=get_password_hash("Demo@12345"),
                role=RoleEnum.CITIZEN,
                # phone_number is not in the User model! Let's remove it
            )
            db.add(demo_citizen)
            print("Seeded Demo Citizen: demo@risklens.local / Demo@12345")
            
        # Seed Demo Officer
        demo_officer = db.query(Officer).filter(Officer.email == "officer@risklens.local").first()
        if not demo_officer:
            demo_officer = Officer(
                id=str(uuid.uuid4()),
                firebase_uid=str(uuid.uuid4()),  # In local mode this is sub
                name="Demo Officer", # Added name which is required
                email="officer@risklens.local",
                password_hash=get_password_hash("Officer@123"),
                role=RoleEnum.OFFICER,
                department_id="TRAFFIC_NMC",
                is_active=True
            )
            db.add(demo_officer)
            print("Seeded Demo Officer: officer@risklens.local / Officer@123")

        db.commit()

        # Seed Routing Rules
        from app.modules.routing.models import RoutingRule
        rules = [
            {"category": "Road", "department_id": "TRAFFIC_NMC", "evaluation_priority": 10},
            {"category": "Traffic", "department_id": "TRAFFIC_NMC", "evaluation_priority": 10},
            {"category": "FALLBACK", "department_id": "DEPT_GENERAL_ADMIN", "evaluation_priority": 0}
        ]
        
        for rule_data in rules:
            existing = db.query(RoutingRule).filter(RoutingRule.category == rule_data["category"]).first()
            if not existing:
                new_rule = RoutingRule(
                    id=str(uuid.uuid4()),
                    category=rule_data["category"],
                    department_id=rule_data["department_id"],
                    evaluation_priority=rule_data["evaluation_priority"]
                )
                db.add(new_rule)
                print(f"Seeded RoutingRule: {rule_data['category']} -> {rule_data['department_id']}")

        db.commit()
        print("Demo data seeded successfully.")
    except Exception as e:
        print(f"Error seeding demo data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo()
