from sqlalchemy.orm import Session
import json
import uuid
from ai.duplicate_detection.embeddings import generate_embedding
from ai.duplicate_detection.similarity import cosine_similarity
from ai.duplicate_detection.candidate_search import get_geo_candidates
from app.modules.incidents.models import Incident, IncidentStatus
from ai.config import config
from sqlalchemy import func

def process_complaint_clustering(db: Session, complaint) -> Incident | None:
    """
    End-to-end clustering pipeline:
    1. Generate embedding for the new complaint
    2. Search candidates (Geo + Time + Category)
    3. Calculate semantic similarity
    4. Link to existing Incident or create a new one
    """
    
    # 1. Generate embedding
    embedding_input = f"Category: {complaint.category}. Description: {complaint.description}. Address: {complaint.address}"
    embedding_vector = generate_embedding(embedding_input)
    
    # Save embedding to complaint for future comparisons
    complaint.vector_embedding = json.dumps(embedding_vector)
    
    # 2. Find geographic & temporal candidates
    candidates = get_geo_candidates(db, complaint.longitude, complaint.latitude, config.duplicate_time_window_hours)
    
    best_match_incident_id = None
    highest_similarity = 0.0
    
    # 3. Calculate semantic similarity
    for candidate in candidates:
        if not candidate.vector_embedding:
            continue
            
        candidate_vector = json.loads(candidate.vector_embedding)
        sim = cosine_similarity(embedding_vector, candidate_vector)
        
        if sim > highest_similarity:
            highest_similarity = sim
            best_match_incident_id = candidate.incident_id
            
    # 4. Link or Review
    if highest_similarity >= config.duplicate_similarity_auto_link and best_match_incident_id:
        # Link to existing incident
        incident = db.query(Incident).filter(Incident.id == best_match_incident_id).first()
        if incident:
            complaint.incident_id = incident.id
            incident.report_count += 1
            incident.last_reported_at = complaint.created_at
            
            # Update centroid (simplified: just keep original or ideally we'd do ST_Centroid of all points)
            # For MVP we leave the centroid as the first reported location
            
            db.commit()
            return incident
            
    elif highest_similarity >= config.duplicate_similarity_review and best_match_incident_id:
        # TODO: Potential Duplicate Queue.
        # For now, we leave the complaint independent (incident_id = NULL or new Incident)
        # and maybe flag it in a review table. We will create a new Incident for now.
        pass
        
    # Create new Incident
    incident_code = f"INC-{uuid.uuid4().hex[:6].upper()}"
    new_incident = Incident(
        id=str(uuid.uuid4()),
        incident_code=incident_code,
        category=complaint.category,
        latitude=complaint.latitude,
        longitude=complaint.longitude
    )
    db.add(new_incident)
    db.flush() # flush to get the id
    
    complaint.incident_id = new_incident.id
    db.commit()
    
    return new_incident
