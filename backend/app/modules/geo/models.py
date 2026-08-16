from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    
    # Fallback to String instead of MultiPolygon for MVP without PostGIS
    boundary = Column(String, nullable=True)
    
    wards = relationship("Ward", back_populates="zone")

class Ward(Base):
    __tablename__ = "wards"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    zone_id = Column(String, ForeignKey("zones.id"), nullable=False)
    
    # Fallback to String instead of MultiPolygon for MVP without PostGIS
    boundary = Column(String, nullable=True)
    
    zone = relationship("Zone", back_populates="wards")
