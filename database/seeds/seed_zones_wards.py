import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.core.firebase import get_firestore_client

zones = {
    "ZONE_01": {
        "name": "Zone 1 (Laxmi Nagar)",
        "code": "ZONE_01",
        "isActive": True
    },
    "ZONE_02": {
        "name": "Zone 2 (Dharampeth)",
        "code": "ZONE_02",
        "isActive": True
    }
}

wards = {
    "WARD_001": {
        "name": "Ward 1",
        "zoneId": "ZONE_01",
        "code": "WARD_001",
        "isActive": True
    },
    "WARD_002": {
        "name": "Ward 2",
        "zoneId": "ZONE_02",
        "code": "WARD_002",
        "isActive": True
    }
}

def seed_zones_wards():
    db = get_firestore_client()
    batch = db.batch()
    
    for zone_id, zone_data in zones.items():
        doc_ref = db.collection('zones').document(zone_id)
        batch.set(doc_ref, zone_data, merge=True)

    for ward_id, ward_data in wards.items():
        doc_ref = db.collection('wards').document(ward_id)
        batch.set(doc_ref, ward_data, merge=True)
        
    batch.commit()
    print("Zones and Wards seeded successfully.")

if __name__ == "__main__":
    seed_zones_wards()
