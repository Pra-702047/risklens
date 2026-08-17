from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user, CurrentUser
from app.modules.notifications.models import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_user_notifications(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.uid
    ).order_by(Notification.created_at.desc()).all()
    
    return notifications
