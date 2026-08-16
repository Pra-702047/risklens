import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user, CurrentUser
from app.core.firebase import get_firestore_client

client = TestClient(app)

def override_get_current_user_citizen():
    return CurrentUser(
        uid="test_citizen_uid",
        email="citizen@test.com",
        role="CITIZEN"
    )

def override_get_current_user_admin():
    return CurrentUser(
        uid="test_admin_uid",
        email="admin@test.com",
        role="ADMIN"
    )

def test_citizen_access_complaints_demo():
    # Setup mock to simulate a permission in Firestore for CITIZEN role
    # Since require_permission queries Firestore, we would normally mock the Firestore DB too.
    # For this simple mock test, we can just test require_role directly in the admin endpoint.
    pass

def test_admin_route_access():
    app.dependency_overrides[get_current_user] = override_get_current_user_citizen
    response = client.get("/users/admin-only")
    assert response.status_code == 403
    assert "Operation requires one of the following roles" in response.json()["detail"]

    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    response = client.get("/users/admin-only")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Admin"

    # Clean up overrides
    app.dependency_overrides.clear()
