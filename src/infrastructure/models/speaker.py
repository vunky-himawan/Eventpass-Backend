from sqlalchemy import Column, String, DateTime
from ..config.database import Base
import uuid
from sqlalchemy.sql import func

class SpeakerModel(Base):
    __tablename__ = "speakers"

    speaker_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    social_media_links = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())