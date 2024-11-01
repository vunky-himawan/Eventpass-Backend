from sqlalchemy import Column, String, SMALLINT, Text, ForeignKey, DateTime
from ..config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class FeedbackRatingModel(Base):
    __tablename__ = "feedback_ratings"

    feedback_rating_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    participant_id = Column(String(36), ForeignKey("participants.participant_id"), nullable=False)
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    rating_value = Column(SMALLINT, nullable=False)
    rating_feedback = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    participant = relationship("ParticipantModel", back_populates="feedback_ratings")
    event = relationship("EventModel", back_populates="feedback_ratings")