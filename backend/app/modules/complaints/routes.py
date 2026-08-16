from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.dependencies import get_current_user, require_role, CurrentUser
from app.modules.complaints.schemas import ComplaintCreate, ComplaintResponse, AIAnalysisResponse
from app.modules.complaints.service import create_complaint, get_citizen_complaints, get_complaint, add_evidence, save_ai_analysis_draft
from app.services.storage_service import save_evidence
from app.services.ai_client import get_ai_classification

router = APIRouter(prefix="/complaints", tags=["complaints"])

@router.post("/analyze", response_model=AIAnalysisResponse)
async def analyze_complaint_draft(
    description: str = Form(...),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["CITIZEN"]))
):
    # Pass to AI layer. We skip passing the physical file to AI for now, 
    # but the architecture is ready.
    ai_result = get_ai_classification(description, files)
    
    # Save the AI draft Analysis record
    analysis = save_ai_analysis_draft(db, current_user.uid, ai_result)
    
    return AIAnalysisResponse(
        analysis_id=analysis.id,
        predicted_category=analysis.predicted_category,
        confidence=analysis.confidence,
        reason_codes=json.loads(analysis.reason_codes.replace("'", '"')) if analysis.reason_codes else [],
        review_status=analysis.review_status
    )

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def submit_complaint(
    analysis_id: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    longitude: float = Form(...),
    latitude: float = Form(...),
    address: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["CITIZEN"]))
):
    # Assemble structured data
    complaint_data = ComplaintCreate(
        analysis_id=analysis_id,
        category=category,
        description=description,
        longitude=longitude,
        latitude=latitude,
        address=address
    )
    
    # Create the complaint (this validates analysis_id)
    db_complaint = create_complaint(db, complaint_data, current_user)
    
    # Process files if any
    if files:
        for file in files:
            file_url = await save_evidence(file)
            add_evidence(db, db_complaint.id, file_url, file.content_type)
            
    # Refresh to include evidence in response
    db.refresh(db_complaint)
    
    # For MVP response schema, we attach the raw coordinates manually
    db_complaint.longitude = longitude
    db_complaint.latitude = latitude
    
    return db_complaint

@router.get("/", response_model=List[ComplaintResponse])
def get_my_complaints(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["CITIZEN"]))
):
    complaints = get_citizen_complaints(db, current_user)
    
    # Stubbing coordinates out for MVP response formatting 
    # In production, we'd use db.query(Complaint, func.ST_X(Complaint.location)...)
    for c in complaints:
        c.longitude = 0.0
        c.latitude = 0.0
        
    return complaints

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint_detail(
    complaint_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    complaint = get_complaint(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    # Citizens can only view their own
    if current_user.role == "CITIZEN" and complaint.user_id != current_user.uid:
        raise HTTPException(status_code=403, detail="Not authorized to view this complaint")
        
    complaint.longitude = 0.0
    complaint.latitude = 0.0
    return complaint

from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    rating: int
    comment: Optional[str] = None
    resolution_accepted: bool

@router.post("/{complaint_id}/feedback")
def submit_feedback(
    complaint_id: str,
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["CITIZEN"]))
):
    from app.modules.feedback.models import ComplaintFeedback
    from app.modules.field_actions.models import ActionType
    from app.modules.audit.service import log_event
    
    complaint = get_complaint(db, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    if complaint.user_id != current_user.uid:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if complaint.status != ActionType.AWAITING_FEEDBACK:
        raise HTTPException(status_code=400, detail="Complaint is not awaiting feedback")
        
    import uuid
    fb = ComplaintFeedback(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        user_id=current_user.uid,
        rating=feedback.rating,
        comment=feedback.comment,
        resolution_accepted=feedback.resolution_accepted
    )
    db.add(fb)
    
    old_status = complaint.status
    
    if feedback.resolution_accepted:
        complaint.status = ActionType.CLOSED
    else:
        complaint.reopen_count += 1
        if complaint.reopen_count >= 3:
            complaint.status = ActionType.REOPEN_LIMIT_REACHED
        else:
            complaint.status = ActionType.REOPENED
            
    db.commit()
    
    # Audit log
    log_event(db, complaint_id, "CITIZEN_FEEDBACK", old_value=old_status, new_value=complaint.status, actor_id=current_user.uid)
    
    return {"message": "Feedback submitted successfully", "new_status": complaint.status}
