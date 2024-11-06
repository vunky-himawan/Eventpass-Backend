from sqlalchemy import Column, String, ForeignKey, SMALLINT, Enum as SQLAlchemyEnum, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ...config.database import Base
import enum

class Gender(enum.Enum): 
    LAKI_LAKI = "LAKI_LAKI"
    PEREMPUAN = "PEREMPUAN"

class ParticipantModel(Base):
    __tablename__ = "participants"

    participant_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    participant_name = Column(String(255), nullable=False)
    age = Column(SMALLINT, nullable=False)
    gender = Column(SQLAlchemyEnum(Gender), nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("UserModel", back_populates="participant")
    face_embeddings = relationship("FaceEmbeddingModel", back_populates="participant")