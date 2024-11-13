from sqlalchemy import SmallInteger, String, Text, ForeignKey, DateTime
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class FeedbackRatingModel(Base):
    __tablename__ = "feedback_ratings"

    feedback_rating_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    participant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("participants.participant_id"), nullable=False
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.event_id"), nullable=False
    )
    rating_value: Mapped[int] = mapped_column(
        SmallInteger, nullable=False
    )
    rating_feedback: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    participant: Mapped["ParticipantModel"] = relationship(
        "ParticipantModel", back_populates="feedback_ratings"
    )
    event: Mapped["EventModel"] = relationship(
        "EventModel", back_populates="feedback_ratings"
    )
