from sqlalchemy import LargeBinary, String, ForeignKey, BLOB, DateTime
from sqlalchemy.sql import func
from ...config.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

class FaceEmbeddingModel(Base):
    __tablename__ = "face_embeddings"

    face_embedding_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    participant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("participants.participant_id"), nullable=False
    )
    picture_path: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    feature_vector: Mapped[bytes] = mapped_column(
        LargeBinary, nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    participant: Mapped["ParticipantModel"] = relationship(
        "ParticipantModel", back_populates="face_embeddings"
    )
