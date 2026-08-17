import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    if not firebase_admin._apps:
        # Check if we have an explicit path to a service account JSON file
        # or if we are using environment variables
        cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "serviceAccountKey.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'projectId': 'risklens-9f2d4'
            })
        else:
            # Fallback for CI/CD or environments without the key
            firebase_admin.initialize_app(options={'projectId': 'risklens-9f2d4'})

initialize_firebase()

def get_firestore_client():
    return firestore.client()
