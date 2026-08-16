from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, require_role, require_permission, CurrentUser

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_my_profile(current_user: CurrentUser = Depends(get_current_user)):
    return {
        "message": "Authentication successful",
        "user": current_user.dict()
    }

@router.get("/admin-only")
def admin_only_route(current_user: CurrentUser = Depends(require_role(["ADMIN", "SYSTEM_ADMIN"]))):
    return {
        "message": "Welcome Admin",
        "user": current_user.dict()
    }

@router.post("/complaints-demo")
def submit_complaint_demo(current_user: CurrentUser = Depends(require_permission("complaint:create"))):
    return {
        "message": "Complaint creation permission granted",
        "user_id": current_user.uid
    }
