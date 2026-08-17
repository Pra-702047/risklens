from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_role
from app.modules.users.models import User, Officer
from app.modules.routing.models import Department
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def list_users(db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN"]))):
    users = db.query(User).all()
    return users

@router.get("/officers")
def list_officers(db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN", "DEPARTMENT_ADMIN"]))):
    officers = db.query(Officer).all()
    return officers

@router.get("/departments")
def list_departments(db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN"]))):
    deps = db.query(Department).all()
    return deps

class DepartmentCreate(BaseModel):
    id: str
    name: str

@router.post("/departments")
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db), current_user = Depends(require_role(["SYSTEM_ADMIN"]))):
    new_dept = Department(id=dept.id, name=dept.name)
    db.add(new_dept)
    db.commit()
    return new_dept
