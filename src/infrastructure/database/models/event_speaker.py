from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...config.database import Base
import uuid

class EventSpeakerModel(Base):
    __tablename__ = "event_speakers"

    event_speaker_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.event_id"), nullable=False
    )
    speaker_id: Mapped[str] = mapped_column(
                String(36), ForeignKey("speakers.speaker_id"), nullable=False
    )

    event: Mapped["EventModel"] = relationship('EventModel', uselist=False, back_populates="event_speakers")
    speaker: Mapped["SpeakerModel"] = relationship('SpeakerModel', uselist=False, back_populates="event_speakers")


    def to_dict(self):
        return {
            "event_speaker_id": self.event_speaker_id,
            "event_id": self.event_id,
            "speaker_id": self.speaker_id
        }