from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime, timezone
from app.core.database import Base

class IncidentStatus(str):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, index=True)
    incident_code = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    
    # Replaced ST_Centroid with basic floats for MVP without PostGIS
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    status = Column(String, default=IncidentStatus.OPEN, nullable=False)
    
    first_reported_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_reported_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    report_count = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
