from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EvidenceResponse(BaseModel):
    id: str
    file_url: str
    file_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class AIAnalysisResponse(BaseModel):
    analysis_id: str
    predicted_category: str
    confidence: float
    reason_codes: List[str]
    review_status: str

    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    analysis_id: str
    category: str
    description: str
    address: Optional[str] = None
    longitude: float = Field(..., description="GPS Longitude")
    latitude: float = Field(..., description="GPS Latitude")

class ComplaintResponse(BaseModel):
    id: str
    user_id: str
    category: str
    description: str
    address: Optional[str]
    longitude: float
    latitude: float
    status: str
    decision_source: Optional[str]
    created_at: datetime
    updated_at: datetime
    evidence: List[EvidenceResponse] = []

    class Config:
        from_attributes = True
