import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def run_audit():
    results = {}
    
    print("--- 1. Testing Health ---")
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(r.status_code, r.json())
        results['health'] = True
    except Exception as e:
        print(f"Health check failed: {e}")
        results['health'] = False
        return results

    print("\n--- 2. Register Citizen User ---")
    demo_user = {
        "email": f"demo_{int(time.time())}@risklens.local",
        "password": "Demo@12345",
        "role": "CITIZEN"
    }
    
    citizen_token = None
    try:
        r = requests.post(f"{BASE_URL}/users/register", json=demo_user)
        print("Register:", r.status_code, r.text)
        if r.status_code in [200, 201]:
            # Now login
            login_data = {
                "username": demo_user["email"],
                "password": demo_user["password"]
            }
            r_login = requests.post(f"{BASE_URL}/users/login", data=login_data)
            print("Login:", r_login.status_code, r_login.text)
            if r_login.status_code == 200:
                citizen_token = r_login.json().get("access_token")
                results['citizen_auth'] = True
            else:
                results['citizen_auth'] = False
        else:
            results['citizen_auth'] = False
    except Exception as e:
        print(f"Citizen auth failed: {e}")
        results['citizen_auth'] = False

    if not citizen_token:
        print("Failed to get citizen token, skipping citizen tests")
    else:
        print("\n--- 3. Create Complaint ---")
        headers = {"Authorization": f"Bearer {citizen_token}"}
        
        # Test AI Analysis first
        print("Testing AI Analysis...")
        ai_payload = {"description": "Heavy traffic congestion reported near a major junction in Nagpur."}
        ai_result = None
        try:
            r = requests.post(f"{BASE_URL}/complaints/analyze", data=ai_payload, headers=headers)
            print("Analyze:", r.status_code, r.text)
            if r.status_code == 200:
                ai_result = r.json()
                results['ai_analysis'] = True
            else:
                results['ai_analysis'] = False
        except Exception as e:
            print(f"AI Analysis failed: {e}")
            results['ai_analysis'] = False

        # Submit Complaint
        print("Submitting Complaint...")
        complaint_payload = {
            "description": "Heavy traffic congestion reported near a major junction in Nagpur.",
            "category": "TRAFFIC_JAM",
            "latitude": "21.1458",
            "longitude": "79.0882",
            "address": "Nagpur Center"
        }
        if ai_result:
            complaint_payload["analysis_id"] = ai_result.get("analysis_id", "")

        complaint_id = None
        try:
            r = requests.post(f"{BASE_URL}/complaints/", data=complaint_payload, headers=headers)
            print("Submit Complaint:", r.status_code, r.text)
            if r.status_code == 200:
                complaint_id = r.json().get("id")
                results['create_complaint'] = True
            else:
                results['create_complaint'] = False
        except Exception as e:
            print(f"Submit complaint failed: {e}")
            results['create_complaint'] = False
            
        print("\n--- 4. Check Citizen Dashboard ---")
        try:
            r = requests.get(f"{BASE_URL}/complaints/", headers=headers)
            print("Citizen Dashboard:", r.status_code, r.text[:200])
            if r.status_code == 200:
                results['citizen_dashboard'] = True
            else:
                results['citizen_dashboard'] = False
        except Exception as e:
            print(f"Dashboard failed: {e}")
            results['citizen_dashboard'] = False

    print("\n--- 5. Officer Flow ---")
    officer_token = None
    # Use dev officer login to get token
    try:
        # Based on the mocked officer portal we saw earlier: "dev_road_officer_uid"
        # However, backend uses proper auth. Let's see if we can register an officer or use a seed one.
        officer_user = {
            "email": f"officer_{int(time.time())}@risklens.local",
            "password": "Demo@12345",
            "role": "OFFICER"
        }
        r = requests.post(f"{BASE_URL}/users/register", json=officer_user)
        print("Register Officer:", r.status_code, r.text)
        
        login_data = {
            "username": officer_user["email"],
            "password": officer_user["password"]
        }
        r_login = requests.post(f"{BASE_URL}/users/login", data=login_data)
        print("Login Officer:", r_login.status_code, r_login.text)
        if r_login.status_code == 200:
            officer_token = r_login.json().get("access_token")
            results['officer_auth'] = True
        else:
            results['officer_auth'] = False
    except Exception as e:
        print(f"Officer auth failed: {e}")
        results['officer_auth'] = False

    if officer_token:
        headers_off = {"Authorization": f"Bearer {officer_token}"}
        print("Checking Officer Queue...")
        try:
            r = requests.get(f"{BASE_URL}/officer/complaints/", headers=headers_off)
            print("Officer Queue:", r.status_code, r.text[:200])
            results['officer_queue'] = r.status_code == 200
        except:
            results['officer_queue'] = False
            
        if complaint_id:
            print(f"Update Complaint Status: {complaint_id} to IN_PROGRESS")
            try:
                r = requests.post(f"{BASE_URL}/officer/complaints/{complaint_id}/actions?action_type=IN_PROGRESS", headers=headers_off)
                print("Update Status:", r.status_code, r.text)
                results['officer_action'] = r.status_code == 200
            except:
                results['officer_action'] = False

    print("\n--- 6. Analytics API ---")
    try:
        r = requests.get(f"{BASE_URL}/analytics/dashboard")
        print("Analytics:", r.status_code, r.text[:200])
        results['analytics'] = r.status_code == 200
    except:
        results['analytics'] = False
        
    print("\n--- Summary ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_audit()
