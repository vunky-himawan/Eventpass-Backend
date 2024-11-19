from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    event_details: Mapped["EventDetailModel"] = relationship("EventDetailModel", back_populates="speaker", cascade="all, delete-orphan")

