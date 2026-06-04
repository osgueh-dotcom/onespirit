from sqlalchemy import Column, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Task(Base, BaseModelMixin):
    __tablename__ = "tasks"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="tasks")

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    
    status = Column(String(50), nullable=False, default="todo")  # todo, in_progress, review, done
    priority = Column(String(50), nullable=False, default="medium")  # low, medium, high

    assigned_to_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])

    created_by_id = Column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_by = relationship("User", foreign_keys=[created_by_id])
