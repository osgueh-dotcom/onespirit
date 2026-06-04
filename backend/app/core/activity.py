import uuid
from sqlalchemy.orm import Session
from app.models.activity import ActivityLog

def log_activity(
    db: Session, 
    user_id: str, 
    action: str, 
    entity_type: str, 
    entity_id: str = None, 
    details: dict = None
) -> ActivityLog:
    """Standardized transactional logging utility for One Spirit & Copilot Gueh ecosystem"""
    try:
        # Convert string user_id to uuid.UUID object for SQLite/PostgreSQL compatibility
        parsed_user_id = None
        if user_id:
            if isinstance(user_id, str):
                try:
                    parsed_user_id = uuid.UUID(user_id)
                except ValueError:
                    parsed_user_id = None
            else:
                parsed_user_id = user_id

        log = ActivityLog(
            user_id=parsed_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            details=details or {}
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        # Non-blocking log failure
        print(f"Warning: Central activity logging failed: {str(e)}")
        return None
