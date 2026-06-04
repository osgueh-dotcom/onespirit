from sqlalchemy import Column, ForeignKey, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class EventSchedule(Base, BaseModelMixin):
    __tablename__ = "event_schedules"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="event_schedules")

    venue_name = Column(String(150), nullable=False)
    address = Column(Text, nullable=True)
    map_link = Column(String(255), nullable=True)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    rundown = Column(JSON, nullable=False, default=list)  # List of items: [{"time": "08:00", "activity": "Gathering", "pic": "John", "notes": "..."}]

    pic_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    pic = relationship("User")
