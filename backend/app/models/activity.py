from sqlalchemy import Column, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class ActivityLog(Base, BaseModelMixin):
    __tablename__ = "activity_logs"

    user_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User")

    action = Column(String(50), nullable=False)  # project_created, status_transitioned, etc.
    entity_type = Column(String(50), nullable=False)  # project, customer, task, invoice, document
    entity_id = Column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True) # Let's make it more general or keep it as standard column
    
    # Let's keep entity_id as generic UUID or String to support multiple entity tables. 
    # Since we can't have multiple ForeignKeys on a single column, we represent it as simple string or UUID column.
    # String(50) is extremely robust as it can hold any UUID or custom string ID!
    entity_id = Column(String(50), nullable=True) 

    details = Column(JSON, nullable=False, default=dict)
