from sqlalchemy import Column, String, Text, Boolean
from app.core.database import Base
from app.models.base import BaseModelMixin

class EventSource(Base, BaseModelMixin):
    __tablename__ = "event_sources"

    source_type = Column(String(50), nullable=False)  # Hotel, Direct, Repeater, Partner, Instagram, Web, Other
    vendor_name = Column(String(100), nullable=True)
    sales_name = Column(String(100), nullable=True)
    contact = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
