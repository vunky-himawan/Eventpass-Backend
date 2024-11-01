from sqlalchemy import Column, String, ForeignKey, BLOB, DateTime
from sqlalchemy.sql import func
from ..config.database import Base
import uuid
from sqlalchemy.orm import relationship

class FaceEmbeddingModel(Base):
    __tablename__ = "face_embeddings"

    face_embedding_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    participant_id = Column(String(36), ForeignKey("participants.participant_id"), nullable=False)
    picture_path = Column(String(255), nullable=False)
    feature_vector = Column(BLOB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    participant = relationship("ParticipantModel", back_populates="face_embeddings")