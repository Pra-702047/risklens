import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from app.core.firebase import get_firestore_client

departments = {
    "DEPT_TRAFFIC": {
        "name": "Traffic Operations",
        "code": "TRAFFIC",
        "description": "Traffic-related operational complaints",
        "isActive": True,
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    },
    "DEPT_SANITATION": {
        "name": "Sanitation",
        "code": "SANITATION",
        "description": "Waste management and sanitation",
        "isActive": True,
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    }
}

def seed_departments():
    db = get_firestore_client()
    batch = db.batch()
    
    for dept_id, dept_data in departments.items():
        doc_ref = db.collection('departments').document(dept_id)
        batch.set(doc_ref, dept_data, merge=True)
        
    batch.commit()
    print("Departments seeded successfully.")

if __name__ == "__main__":
    seed_departments()
