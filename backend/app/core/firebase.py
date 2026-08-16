import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    if not firebase_admin._apps:
        # Check if we have an explicit path to a service account JSON file
        # or if we are using environment variables
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
        else:
            # For testing/mocking, or relying on default application credentials
            # Alternatively, load individual env vars for a dict credential if needed
            # cred = credentials.Certificate({
            #     "type": "service_account",
            #     "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            #     "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
            #     "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            # })
            cred = credentials.ApplicationDefault()
            
        firebase_admin.initialize_app(cred)

initialize_firebase()

def get_firestore_client():
    return firestore.client()
