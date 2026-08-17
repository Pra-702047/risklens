import requests
import time

BASE_URL = "http://localhost:8000"

def run_test():
    print("=== RiskLens E2E Verification ===")
    
    # 1. Citizen Login
    print("1. Citizen Login")
    r = requests.post(f"{BASE_URL}/users/login", json={"username": "demo@risklens.local", "password": "Demo@12345"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    citizen_token = r.json()["access_token"]
    citizen_headers = {"Authorization": f"Bearer {citizen_token}"}
    
    # 2. Analyze Complaint
    print("2. Analyze Complaint")
    analyze_data = {
        "description": "Large pothole causing traffic issues on Main Street."
    }
    r = requests.post(f"{BASE_URL}/complaints/analyze", data=analyze_data, headers=citizen_headers)
    assert r.status_code == 200, f"Analyze failed: {r.text}"
    analysis_id = r.json()["analysis_id"]
    print(f"   Analysis ID: {analysis_id}")

    # 3. Submit Complaint
    print("3. Submit Complaint")
    complaint_data = {
        "analysis_id": analysis_id,
        "category": "Road",
        "description": "Large pothole causing traffic issues on Main Street.",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "address": "Main Street, Nagpur",
        "is_anonymous": False
    }
    r = requests.post(f"{BASE_URL}/complaints/", data=complaint_data, headers=citizen_headers)
    assert r.status_code == 201, f"Submit failed: {r.text}"
    complaint_id = r.json()["id"]
    print(f"   Created complaint: {complaint_id}")
    
    # Wait for background routing / AI
    time.sleep(2)
    
    # 4. Officer Login
    print("4. Officer Login")
    r = requests.post(f"{BASE_URL}/users/login", json={"username": "officer@risklens.local", "password": "Officer@123"})
    assert r.status_code == 200, f"Officer login failed: {r.text}"
    officer_token = r.json()["access_token"]
    officer_headers = {"Authorization": f"Bearer {officer_token}"}
    
    # 5. Officer Views Complaints
    print("5. Officer Views Assigned Complaints")
    r = requests.get(f"{BASE_URL}/officer/complaints/", headers=officer_headers)
    assert r.status_code == 200
    complaints = r.json()
    assert any(c["id"] == complaint_id for c in complaints), "Complaint not routed to officer!"
    
    # 6. Officer Claims
    print("6. Officer Claims Complaint")
    r = requests.post(f"{BASE_URL}/officer/complaints/{complaint_id}/claim", headers=officer_headers)
    assert r.status_code == 200, f"Claim failed: {r.text}"
    
    # 7. Officer Adds Action
    print("7. Officer Adds Action")
    action_data = {
        "action_type": "IN_PROGRESS",
        "notes": "Team dispatched.",
        "media_urls": []
    }
    r = requests.post(f"{BASE_URL}/officer/complaints/{complaint_id}/actions", json=action_data, headers=officer_headers)
    assert r.status_code == 200, f"Action failed: {r.text}"
    
    # 8. Officer Resolves
    print("8. Officer Resolves Complaint")
    resolve_data = {
        "action_type": "RESOLVED",
        "notes": "Pothole filled.",
        "media_urls": []
    }
    r = requests.post(f"{BASE_URL}/officer/complaints/{complaint_id}/actions", json=resolve_data, headers=officer_headers)
    assert r.status_code == 200, f"Resolve failed: {r.text}"
    
    # 9. Citizen views timeline
    print("9. Citizen Checks Timeline")
    r = requests.get(f"{BASE_URL}/complaints/{complaint_id}", headers=citizen_headers)
    assert r.status_code == 200
    details = r.json()
    assert details["status"] == "AWAITING_FEEDBACK", f"Expected AWAITING_FEEDBACK, got {details['status']}"
    assert len(details.get("status_history", [])) > 0, "No status history found!"
    
    # 10. Citizen submits feedback
    print("10. Citizen Submits Feedback")
    r = requests.post(f"{BASE_URL}/complaints/{complaint_id}/feedback", json={"rating": 5, "comments": "Good job"}, headers=citizen_headers)
    assert r.status_code == 200, f"Feedback failed: {r.text}"
    
    r = requests.get(f"{BASE_URL}/complaints/{complaint_id}", headers=citizen_headers)
    details = r.json()
    assert details["status"] == "CLOSED", "Complaint should be CLOSED after feedback"
    
    print("=== All tests passed! Backend E2E is fully verified. ===")

if __name__ == "__main__":
    run_test()
