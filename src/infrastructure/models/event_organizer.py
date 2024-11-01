from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from ..config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class EventOrganizerModel(Base):
    __tablename__ = "event_organizers"

    event_organizer_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone_number = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("UserModel", back_populates="event_organizers")