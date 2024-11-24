from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...config.database import Base
import uuid

class EventSpeakerModel(Base):
    __tablename__ = "event_details"

    event_speaker_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.event_id"), nullable=False
    )
    speaker_id: Mapped[str] = mapped_column(
                String(36), ForeignKey("speakers.speaker_id"), nullable=False
    )

    event: Mapped["EventModel"] = relationship(
            "EventModel",
            back_populates="event_speakers",
            lazy="joined",
    )
    speaker: Mapped["SpeakerModel"] = relationship(
            "SpeakerModel",
            back_populates="event_speakers",
            lazy="joined",
    )
