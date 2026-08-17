import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"

def run_audit():
    results = {
        "health": False,
        "auth_citizen": False,
        "auth_officer": False,
        "complaint_creation": False,
        "ai_analysis": False,
        "citizen_dashboard": False,
        "officer_queue": False,
        "officer_action": False,
        "gis": False,
        "analytics": False,
        "admin": False,
        "notifications": False
    }

    print("--- Testing API Health ---")
    try:
        r = requests.get(f"{BASE_URL}/health")
        if r.status_code == 200:
            results["health"] = True
            print("OK")
    except:
        pass

    print("\n--- Testing Citizen Workflow ---")
    # Backend allows 'mock_token' to bypass firebase for CITIZEN testing
    headers_citizen = {"Authorization": "Bearer mock_token"}
    
    # 1. AI Analysis
    ai_payload = {"description": "Heavy traffic jam near central market."}
    ai_analysis_id = None
    try:
        r = requests.post(f"{BASE_URL}/complaints/analyze", data=ai_payload, headers=headers_citizen)
        print("AI Analyze:", r.status_code, r.text)
        if r.status_code == 200:
            results["ai_analysis"] = True
            ai_analysis_id = r.json().get("analysis_id")
    except Exception as e:
        print("AI Error:", e)

    # 2. Submit Complaint
    complaint_payload = {
        "description": "Heavy traffic jam near central market.",
        "category": "TRAFFIC_JAM",
        "latitude": "21.1458",
        "longitude": "79.0882",
        "address": "Central Market"
    }
    if ai_analysis_id:
        complaint_payload["analysis_id"] = ai_analysis_id
        
    complaint_id = None
    try:
        r = requests.post(f"{BASE_URL}/complaints/", data=complaint_payload, headers=headers_citizen)
        print("Submit:", r.status_code, r.text)
        if r.status_code == 200:
            results["complaint_creation"] = True
            complaint_id = r.json().get("id")
    except Exception as e:
        print("Submit Error:", e)

    # 3. Citizen Dashboard
    try:
        r = requests.get(f"{BASE_URL}/complaints/", headers=headers_citizen)
        print("Citizen Dashboard:", r.status_code, r.text[:200])
        if r.status_code == 200:
            results["citizen_dashboard"] = True
    except:
        pass

    print("\n--- Testing Officer Workflow ---")
    # Officer login in frontend uses a mocked JWT containing their UID. 
    # Backend dependencies.py checks verify_firebase_token. If token is "mock_token", it returns "mock_uid".
    # But for an officer to work, they must exist in the Officer table with firebase_uid="mock_uid".
    # Let's seed it.
    print("Attempting to test officer with 'mock_token'")
    headers_officer = {"Authorization": "Bearer mock_token"}
    
    try:
        r = requests.get(f"{BASE_URL}/officer/complaints/", headers=headers_officer)
        print("Officer Queue:", r.status_code, r.text[:200])
        if r.status_code == 200:
            results["officer_queue"] = True
        else:
            print("Officer not found in DB with mock_uid")
    except:
        pass
        
    if complaint_id:
        try:
            r = requests.post(f"{BASE_URL}/officer/complaints/{complaint_id}/actions?action_type=IN_PROGRESS", headers=headers_officer)
            print("Officer Action:", r.status_code, r.text)
            if r.status_code == 200:
                results["officer_action"] = True
        except:
            pass

    print("\n--- Testing Other APIs ---")
    try:
        r = requests.get(f"{BASE_URL}/analytics/dashboard", headers=headers_officer)
        print("Analytics:", r.status_code, r.text[:100])
        if r.status_code == 200:
            results["analytics"] = True
    except:
        pass
        
    print("\n--- Audit Results ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_audit()
