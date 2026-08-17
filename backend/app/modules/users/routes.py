from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, require_role, require_permission, CurrentUser
from app.core.database import get_db
from app.modules.users.models import User, RoleEnum, Officer
from app.core.security import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel, EmailStr
import uuid

router = APIRouter(prefix="/users", tags=["users"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "CITIZEN"

class UserLogin(BaseModel):
    username: str
    password: str

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/register")
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        officer = db.query(Officer).filter(Officer.email == user_in.email).first()
        if officer:
            raise HTTPException(status_code=400, detail="Email already registered as officer")
            
        # Create user
        valid_roles = [RoleEnum.CITIZEN, RoleEnum.OFFICER, RoleEnum.DEPARTMENT_ADMIN, RoleEnum.SUPERVISOR, RoleEnum.SYSTEM_ADMIN]
        role_to_set = user_in.role if user_in.role in valid_roles else RoleEnum.CITIZEN
        
        new_user = User(
            id=str(uuid.uuid4()),
            email=user_in.email,
            password_hash=get_password_hash(user_in.password),
            role=role_to_set,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"message": "User registered successfully", "id": new_user.id}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    # Check User (Citizen)
    user = db.query(User).filter(User.email == user_in.username).first()
    if user and verify_password(user_in.password, user.password_hash):
        token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
        return {"access_token": token, "token_type": "bearer", "role": user.role}
        
    # Check Officer
    officer = db.query(Officer).filter(Officer.email == user_in.username).first()
    if officer and officer.password_hash and verify_password(user_in.password, officer.password_hash):
        token = create_access_token(data={"sub": officer.firebase_uid, "email": officer.email, "role": officer.role})
        return {"access_token": token, "token_type": "bearer", "role": officer.role}

    raise HTTPException(status_code=401, detail="Incorrect email or password")

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
