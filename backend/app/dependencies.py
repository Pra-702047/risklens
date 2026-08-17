from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_firebase_token
from app.modules.users.models import Officer, RoleEnum
from pydantic import BaseModel
from typing import Optional

security = HTTPBearer()

class CurrentUser(BaseModel):
    uid: str
    email: Optional[str] = None
    phone_number: Optional[str] = None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> CurrentUser:
    token = credentials.credentials
    try:
        decoded_token = verify_firebase_token(token)
        uid = decoded_token.get("uid")
        
        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain a valid UID",
            )
            
        return CurrentUser(
            uid=uid,
            email=decoded_token.get("email"),
            phone_number=decoded_token.get("phone_number")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}"
        )

def get_current_officer(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Officer:
    officer = db.query(Officer).filter(
        Officer.firebase_uid == current_user.uid,
        Officer.is_active == True
    ).first()
    
    if not officer:
        raise HTTPException(status_code=403, detail="Access denied. Officer profile not found or inactive.")
        
    if officer.role not in [RoleEnum.OFFICER, RoleEnum.SUPERVISOR, RoleEnum.DEPARTMENT_ADMIN, RoleEnum.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Access denied. Insufficient role permissions.")
        
    return officer

def require_role(roles: list[str]):
    def role_checker(current_user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
        from app.modules.users.models import Officer, User
        
        # Check officers table first
        officer = db.query(Officer).filter(Officer.firebase_uid == current_user.uid).first()
        if officer and officer.role in roles:
            return current_user
            
        # Check citizens/users table
        user = db.query(User).filter(User.id == current_user.uid).first()
        if user and user.role in roles:
            return current_user
            
        raise HTTPException(status_code=403, detail="Access denied. Required role not found.")
    return role_checker

def require_permission(permission: str):
    # Dummy implementation for now to satisfy imports
    def permission_checker(current_user: CurrentUser = Depends(get_current_user)):
        return current_user
    return permission_checker
