from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ...config.database import Base
import uuid
from sqlalchemy.sql import func

class SpeakerModel(Base):
    __tablename__ = "speakers"

    speaker_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    social_media_links: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    company: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    event_speakers: Mapped[List["EventSpeakerModel"]] = relationship('EventSpeakerModel', uselist=True, back_populates="speaker")

    def to_dict(self):
        return {
            "speaker_id": self.speaker_id,
            "name": self.name,
            "title": self.title,
            "social_media_links": self.social_media_links,
            "company": self.company,
            "created_at": self.created_at
        }