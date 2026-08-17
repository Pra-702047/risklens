from sqlalchemy.orm import Session
from app.modules.complaints.models import Complaint, Evidence, ComplaintStatus, ComplaintAIAnalysis, DecisionSource, AnalysisStatus, ReviewStatus
from app.modules.complaints.schemas import ComplaintCreate
from app.utils.id_generator import generate_complaint_id
from app.dependencies import CurrentUser
import uuid
from fastapi import HTTPException
import json

# New pipeline imports
from app.services.geo_service import get_zone_and_ward_for_point
from app.modules.routing.service import get_routing_for_complaint
from ai.duplicate_detection.clustering import process_complaint_clustering
from app.modules.severity.service import generate_and_save_severity
from app.modules.sla.service import calculate_and_assign_sla
from app.modules.audit.service import log_event
from app.modules.audit.models import EventType

def save_ai_analysis_draft(db: Session, uid: str, ai_result: dict) -> ComplaintAIAnalysis:
    analysis_id = f"AI-ANL-{uuid.uuid4().hex[:8].upper()}"
    
    # Determine review status
    from ai.config import config
    confidence = ai_result.get("confidence", 0.0)
    if confidence >= config.auto_accept_threshold:
        review_status = ReviewStatus.AUTO_ACCEPTED.value
    else:
        review_status = ReviewStatus.HUMAN_REVIEW.value
        
    db_analysis = ComplaintAIAnalysis(
        id=analysis_id,
        firebase_uid=uid,
        predicted_category=ai_result.get("predicted_category"),
        subcategory=ai_result.get("subcategory"),
        confidence=confidence,
        reason_codes=json.dumps(ai_result.get("reason_codes", [])),
        review_status=review_status,
        analysis_status=AnalysisStatus.PENDING_DRAFT.value,
        model_provider=ai_result.get("model_provider"),
        model=ai_result.get("model"),
        model_version=ai_result.get("model_version")
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def create_complaint(db: Session, complaint_in: ComplaintCreate, current_user: CurrentUser) -> Complaint:
    # Verify AI Analysis
    analysis = db.query(ComplaintAIAnalysis).filter(
        ComplaintAIAnalysis.id == complaint_in.analysis_id,
        ComplaintAIAnalysis.firebase_uid == current_user.uid,
        ComplaintAIAnalysis.analysis_status.in_([AnalysisStatus.PENDING_DRAFT.value, AnalysisStatus.FAILED.value])
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=400, detail="Invalid or expired AI analysis ID")

    # Determine decision source
    if complaint_in.category == analysis.predicted_category:
        decision_source = DecisionSource.CITIZEN_CONFIRMED.value
        analysis.analysis_status = AnalysisStatus.CONFIRMED.value
    else:
        decision_source = DecisionSource.CITIZEN_OVERRIDE.value
        analysis.analysis_status = AnalysisStatus.OVERRIDDEN.value

    # Generate unique ID
    complaint_id = generate_complaint_id()
    
    # Create preliminary complaint instance
    db_complaint = Complaint(
        id=complaint_id,
        user_id=current_user.uid,
        category=complaint_in.category,
        description=complaint_in.description,
        address=complaint_in.address,
        latitude=complaint_in.latitude,
        longitude=complaint_in.longitude,
        status=ComplaintStatus.SUBMITTED.value,
        decision_source=decision_source,
        analysis_id=analysis.id
    )
    
    analysis.complaint_id = complaint_id
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    log_event(db, complaint_id, EventType.COMPLAINT_CREATED, new_value=complaint_id, actor_id=current_user.uid)
    
    from app.modules.complaints.service import log_status_change
    log_status_change(db, complaint_id, None, ComplaintStatus.SUBMITTED.value, current_user.uid, "Citizen submitted complaint")
    
    # (Volatile fields not needed as they are now real columns)
    
    # PIPELINE EXECUTION (Synchronous MVP)
    
    # STEP 1: GIS Location
    zone, ward = get_zone_and_ward_for_point(db, complaint_in.longitude, complaint_in.latitude)
    zone_id = zone.id if zone else None
    db_complaint.ward_id = ward.id if ward else None
    db.commit()
    
    # STEP 2: Incident Detection
    incident = process_complaint_clustering(db, db_complaint)
    
    # STEP 3: Severity Scoring
    severity = generate_and_save_severity(db, complaint_id, db_complaint.category, db_complaint.description, db_complaint.address)
    db_complaint.priority = severity.priority
    db.commit()
    log_event(db, complaint_id, EventType.PRIORITY_ASSIGNED, new_value=severity.priority)
    
    # STEP 4: Department Routing (Now Priority Aware)
    department_id = get_routing_for_complaint(db, db_complaint.category, zone_id, db_complaint.priority)
    db_complaint.department_id = department_id
    db.commit()
    log_event(db, complaint_id, EventType.ROUTE_ASSIGNED, new_value=department_id)
    
    # Auto Assign Officer
    from app.modules.routing.service import auto_assign_officer
    auto_assign_officer(db, complaint_id, department_id, zone_id)
    
    
    # STEP 5: SLA Calculation
    sla_status = calculate_and_assign_sla(db, complaint_id, db_complaint.priority)
    log_event(db, complaint_id, EventType.SLA_STARTED, new_value=sla_status.due_at.isoformat())
    
    db.refresh(db_complaint)
    return db_complaint

def add_evidence(db: Session, complaint_id: str, file_data: bytes, mime_type: str, file_type: str) -> Evidence:
    evidence_id = str(uuid.uuid4())
    file_url = f"http://127.0.0.1:8000/complaints/evidence/{evidence_id}" # Static for MVP
    
    db_evidence = Evidence(
        id=evidence_id,
        complaint_id=complaint_id,
        file_url=file_url,
        file_data=file_data,
        mime_type=mime_type,
        file_size=len(file_data),
        file_type=file_type
    )
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence

def get_citizen_complaints(db: Session, current_user: CurrentUser):
    # Retrieve complains + coordinates (using ST_X and ST_Y from PostGIS if needed, but for MVP returning ORM)
    return db.query(Complaint).filter(Complaint.user_id == current_user.uid).all()

def get_complaint(db: Session, complaint_id: str):
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()

def log_status_change(db: Session, complaint_id: str, from_status: str, to_status: str, user_id: str, notes: str = None):
    from app.modules.complaints.models import ComplaintStatusHistory
    history = ComplaintStatusHistory(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        from_status=from_status,
        to_status=to_status,
        changed_by_user_id=user_id,
        notes=notes
    )
    db.add(history)
    db.commit()
