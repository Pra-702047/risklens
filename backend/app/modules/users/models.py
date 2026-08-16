from sqlalchemy import Column, String, Boolean, DateTime, ARRAY
from datetime import datetime, timezone
from app.core.database import Base

class RoleEnum(str):
    CITIZEN = "CITIZEN"
    OFFICER = "OFFICER"
    SUPERVISOR = "SUPERVISOR"
    DEPARTMENT_ADMIN = "DEPARTMENT_ADMIN"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"

class Officer(Base):
    __tablename__ = "officers"
    
    id = Column(String, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default=RoleEnum.OFFICER, nullable=False)
    
    department_id = Column(String, nullable=False, index=True)
    team_id = Column(String, nullable=True)
    zone_ids = Column(ARRAY(String), nullable=True) # Postgres ARRAY type
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
