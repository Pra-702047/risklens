import sys
import os

# Add backend to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from app.core.firebase import get_firestore_client

roles = {
    "CITIZEN": {
        "name": "CITIZEN",
        "description": "Citizen user",
        "permissions": [
            "complaint:create",
            "complaint:read:own",
            "feedback:create"
        ]
    },
    "OFFICER": {
        "name": "OFFICER",
        "description": "Field Officer",
        "permissions": [
            "complaint:read:assigned",
            "complaint:update",
            "evidence:create",
            "complaint:resolve"
        ]
    },
    "SUPERVISOR": {
        "name": "SUPERVISOR",
        "description": "Department Supervisor",
        "permissions": [
            "complaint:read:team",
            "assignment:create",
            "assignment:update",
            "sla:read"
        ]
    },
    "ADMIN": {
        "name": "ADMIN",
        "description": "Department Admin",
        "permissions": [
            "complaint:read:all",
            "department:read",
            "department:manage",
            "routing:read",
            "routing:manage",
            "sla:read",
            "sla:manage",
            "analytics:read"
        ]
    },
    "SYSTEM_ADMIN": {
        "name": "SYSTEM_ADMIN",
        "description": "System Administrator",
        "permissions": [
            "user:read",
            "user:manage",
            "role:read",
            "role:manage"
        ]
    },
    "AUDITOR": {
        "name": "AUDITOR",
        "description": "Read-only Auditor",
        "permissions": [
            "complaint:read:all",
            "sla:read",
            "audit:read",
            "analytics:read"
        ]
    }
}

def seed_roles():
    db = get_firestore_client()
    batch = db.batch()
    
    for role_id, role_data in roles.items():
        doc_ref = db.collection('roles').document(role_id)
        batch.set(doc_ref, role_data, merge=True)
        
    batch.commit()
    print("Roles seeded successfully.")

if __name__ == "__main__":
    seed_roles()
