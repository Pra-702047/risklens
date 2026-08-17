import sys
import os
import uuid
# Add project root to sys path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, Base, engine
from app.modules.users.models import Officer, RoleEnum
from app.modules.routing.models import RoutingRule

def seed_data():
    db = SessionLocal()
    
    # 1. Clear existing seed data (optional, but good for idempotency)
    db.query(Officer).filter(Officer.email.like('%@mock.gov.in')).delete()
    db.query(RoutingRule).delete()
    db.commit()

    print("Seeding Officers...")
    officers = [
        Officer(
            id=str(uuid.uuid4()),
            firebase_uid="dev_road_officer_uid",
            name="Ramesh (Road Dept)",
            email="road@mock.gov.in",
            role=RoleEnum.OFFICER,
            department_id="DEPT_ROAD",
            is_active=True
        ),
        Officer(
            id=str(uuid.uuid4()),
            firebase_uid="dev_water_officer_uid",
            name="Suresh (Water Dept)",
            email="water@mock.gov.in",
            role=RoleEnum.OFFICER,
            department_id="DEPT_WATER",
            is_active=True
        ),
        Officer(
            id=str(uuid.uuid4()),
            firebase_uid="dev_sanitation_officer_uid",
            name="Mahesh (Sanitation Dept)",
            email="sanitation@mock.gov.in",
            role=RoleEnum.OFFICER,
            department_id="DEPT_SANITATION",
            is_active=True
        ),
        Officer(
            id=str(uuid.uuid4()),
            firebase_uid="dev_traffic_officer_uid",
            name="Dinesh (Traffic Police)",
            email="traffic@mock.gov.in",
            role=RoleEnum.OFFICER,
            department_id="DEPT_TRAFFIC",
            is_active=True
        )
    ]
    db.add_all(officers)

    print("Seeding Routing Rules...")
    rules = [
        RoutingRule(id=str(uuid.uuid4()), category="POTHOLE", department_id="DEPT_ROAD"),
        RoutingRule(id=str(uuid.uuid4()), category="ROAD_DAMAGE", department_id="DEPT_ROAD"),
        RoutingRule(id=str(uuid.uuid4()), category="ROAD_OBSTRUCTION", department_id="DEPT_ROAD"),
        
        RoutingRule(id=str(uuid.uuid4()), category="WATERLOGGING", department_id="DEPT_WATER"),
        
        RoutingRule(id=str(uuid.uuid4()), category="GARBAGE", department_id="DEPT_SANITATION"),
        
        RoutingRule(id=str(uuid.uuid4()), category="TRAFFIC_JAM", department_id="DEPT_TRAFFIC"),
        RoutingRule(id=str(uuid.uuid4()), category="ROAD_ACCIDENT", department_id="DEPT_TRAFFIC"),
        RoutingRule(id=str(uuid.uuid4()), category="RASH_DRIVING", department_id="DEPT_TRAFFIC"),
        RoutingRule(id=str(uuid.uuid4()), category="ILLEGAL_PARKING", department_id="DEPT_TRAFFIC"),
        RoutingRule(id=str(uuid.uuid4()), category="TRAFFIC_SIGNAL", department_id="DEPT_TRAFFIC"),
        
        # Fallback for others
        RoutingRule(id=str(uuid.uuid4()), category="STREET_LIGHT", department_id="DEPT_ROAD"),
        RoutingRule(id=str(uuid.uuid4()), category="ENCROACHMENT", department_id="DEPT_ROAD"),
        RoutingRule(id=str(uuid.uuid4()), category="OTHER", department_id="DEPT_ROAD")
    ]
    db.add_all(rules)
    
    db.commit()
    print("Seeding Complete!")

if __name__ == "__main__":
    seed_data()
