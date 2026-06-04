from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Document(Base, BaseModelMixin):
    __tablename__ = "documents"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="documents")

    title = Column(String(150), nullable=False)
    file_path = Column(String(255), nullable=False)  # Local path OR Google Drive link
    file_type = Column(String(50), nullable=False)  # pdf, image, link, teaser
    storage_type = Column(String(50), nullable=False)  # local, google_drive
    
    notes = Column(Text, nullable=True)

    uploaded_by_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    uploaded_by = relationship("User")
