from sqlalchemy.orm import Session
from app.modules.notifications.models import Notification, NotificationStatus, NotificationChannel
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger(__name__)

class MockProvider:
    def send(self, channel: str, recipient: str, template_key: str, data: dict) -> dict:
        """
        Mock sending the notification.
        """
        logger.info(f"MOCK_NOTIFICATION | Channel: {channel} | To: {recipient} | Template: {template_key}")
        return {"status": "success", "provider_id": "mock-" + str(uuid.uuid4())}

def dispatch_notification(
    db: Session, 
    complaint_id: str, 
    user_id: str, 
    event_type: str, 
    channel: str, 
    template_key: str, 
    recipient: str,
    data: dict = None
) -> Notification:
    
    # Create DB Record
    notification = Notification(
        id=str(uuid.uuid4()),
        complaint_id=complaint_id,
        user_id=user_id,
        event_type=event_type,
        channel=channel,
        template_key=template_key,
        recipient=recipient,
        status=NotificationStatus.PENDING
    )
    db.add(notification)
    
    # For MVP, execute synchronously inline.
    try:
        provider = MockProvider()
        result = provider.send(channel, recipient, template_key, data or {})
        
        notification.status = NotificationStatus.SENT
        notification.provider = "MOCK"
        notification.sent_at = datetime.now(timezone.utc)
    except Exception as e:
        notification.status = NotificationStatus.FAILED
        notification.error_message = str(e)
        
    db.commit()
    db.refresh(notification)
    return notification
