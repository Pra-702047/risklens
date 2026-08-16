from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, timezone
import enum

class ComplaintStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class DecisionSource(str, enum.Enum):
    AI_AUTO = "AI_AUTO"
    CITIZEN_OVERRIDE = "CITIZEN_OVERRIDE"
    CITIZEN_CONFIRMED = "CITIZEN_CONFIRMED"

class AnalysisStatus(str, enum.Enum):
    PENDING_DRAFT = "PENDING_DRAFT"
    CONFIRMED = "CONFIRMED"
    OVERRIDDEN = "OVERRIDDEN"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class ReviewStatus(str, enum.Enum):
    AUTO_ACCEPTED = "AUTO_ACCEPTED"
    HUMAN_REVIEW = "HUMAN_REVIEW"

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False) # Firebase UID
    category = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    address = Column(String, nullable=True)
    
    # Removed PostGIS point, using floats
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Routing fields
    department_id = Column(String, nullable=True)
    ward_id = Column(String, ForeignKey("wards.id"), nullable=True)
    
    # Priority and SLA
    # Incident Clustering
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=True)
    vector_embedding = Column(Text, nullable=True) # JSON serialized float array for MVP
    
    status = Column(String, default="SUBMITTED", nullable=False)
    
    # Priority and SLA
    priority = Column(String, nullable=True) # P0, P1, P2, P3
    sla_status_id = Column(String, ForeignKey("sla_status.id"), nullable=True)
    
    reopen_count = Column(Integer, default=0, nullable=False)
    
    decision_source = Column(String, nullable=True)
    analysis_id = Column(String, ForeignKey("ai_analysis.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    evidence = relationship("Evidence", back_populates="complaint", cascade="all, delete-orphan")
    ai_analysis = relationship("ComplaintAIAnalysis", foreign_keys=[analysis_id], post_update=True)

class ComplaintAIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(String, primary_key=True, index=True) # e.g. AI-ANL-123
    complaint_id = Column(String, ForeignKey("complaints.id"), nullable=True)
    firebase_uid = Column(String, index=True, nullable=False)
    
    predicted_category = Column(String, nullable=False)
    subcategory = Column(String, nullable=True)
    confidence = Column(Float, nullable=False)
    reason_codes = Column(Text, nullable=True) # JSON array as text
    
    review_status = Column(String, default=ReviewStatus.HUMAN_REVIEW.value)
    analysis_status = Column(String, default=AnalysisStatus.PENDING_DRAFT.value)
    
    model_provider = Column(String, nullable=True)
    model = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    review_status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED
    
    # Audit for Overrides
    overridden = Column(Boolean, default=False)
    override_reason = Column(String, nullable=True)
    overridden_by = Column(String, nullable=True) # Officer/Admin ID
    overridden_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    analyzed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class EvidenceType(str):
    CITIZEN_PHOTO = "CITIZEN_PHOTO"
    CITIZEN_VIDEO = "CITIZEN_VIDEO"
    BEFORE_PHOTO = "BEFORE_PHOTO"
    AFTER_PHOTO = "AFTER_PHOTO"
    RESOLUTION_DOC = "RESOLUTION_DOC"
    OTHER = "OTHER"

class EvidenceVisibility(str):
    CITIZEN_VISIBLE = "CITIZEN_VISIBLE"
    OFFICER_ONLY = "OFFICER_ONLY"

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, index=True)
    complaint_id = Column(String, ForeignKey("complaints.id"), nullable=False)
    field_action_id = Column(String, ForeignKey("field_actions.id"), nullable=True) # Added for tracing actions
    
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False) # e.g. CITIZEN_PHOTO, AFTER_PHOTO
    mime_type = Column(String, nullable=True) # e.g. image/jpeg
    file_size = Column(Integer, nullable=True) # Bytes
    
    visibility = Column(String, default=EvidenceVisibility.OFFICER_ONLY, nullable=False)
    
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    complaint = relationship("Complaint", back_populates="evidence")
