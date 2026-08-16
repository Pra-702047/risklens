from sqlalchemy.orm import Session
from app.modules.complaints.models import Complaint
from app.modules.incidents.models import Incident
from app.utils.id_generator import generate_complaint_id
from ai.duplicate_detection.clustering import process_complaint_clustering
import uuid

def seed_demo_complaints(db: Session):
    print("Seeding Demo Complaints...")
    
    # Simulate an actual user UID (replace with a known UID or keep generic for testing)
    test_uid = "DEMO_USER_UID_123"
    
    # Base location (Nagpur coordinates roughly)
    lat_base, lng_base = 21.1458, 79.0882
    
    complaints_data = [
        # Incident 1 (POTHOLE) - Two complaints very close to each other
        {
            "category": "POTHOLE",
            "description": "Massive pothole causing accidents near the crossing.",
            "address": "Wardha Road Crossing",
            "lat": lat_base,
            "lng": lng_base
        },
        {
            "category": "POTHOLE",
            "description": "Huge crater on the road, cars are getting damaged.",
            "address": "Wardha Road main signal",
            "lat": lat_base + 0.0001, # ~11 meters away
            "lng": lng_base + 0.0001
        },
        
        # Incident 2 (POTHOLE) - Same category, but far away
        {
            "category": "POTHOLE",
            "description": "Pothole near the school gate.",
            "address": "Civil Lines School",
            "lat": lat_base + 0.05, # ~5.5 km away
            "lng": lng_base + 0.05
        },
        
        # Incident 3 (WATERLOGGING)
        {
            "category": "WATERLOGGING",
            "description": "Severe waterlogging after yesterday's rain.",
            "address": "Sitabuldi Market",
            "lat": lat_base - 0.02,
            "lng": lng_base - 0.02
        }
    ]
    
    for c_data in complaints_data:
        complaint_id = generate_complaint_id()
        wkt_location = f"POINT({c_data['lng']} {c_data['lat']})"
        
        complaint = Complaint(
            id=complaint_id,
            user_id=test_uid,
            category=c_data["category"],
            description=c_data["description"],
            address=c_data["address"],
            location=wkt_location
        )
        
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        
        # Hydrate for downstream
        complaint.longitude = c_data["lng"]
        complaint.latitude = c_data["lat"]
        
        # Run through clustering pipeline
        try:
            process_complaint_clustering(db, complaint)
            print(f"Processed complaint {complaint.id} -> Incident {complaint.incident_id}")
        except Exception as e:
            print(f"Error processing clustering for {complaint.id}: {e}")
            
    print("Demo Complaints Seeded Successfully.")

if __name__ == "__main__":
    from app.core.database import SessionLocal
    db = SessionLocal()
    seed_demo_complaints(db)
    db.close()
