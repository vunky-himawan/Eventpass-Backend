from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum as SQLAlchemyEnum
from ...config.database import Base
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

class TransactionCategoryEnum(Enum):
    TIKET = "TIKET"
    TOP_UP = "TOP UP"

class TransactionStatusEnum(Enum):
    BERHASIL = "BERHASIL"
    GAGAL = "GAGAL"

class TransactionModel(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    participant_id = Column(String(36), ForeignKey("participants.participant_id"), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    category = Column(SQLAlchemyEnum(TransactionCategoryEnum), nullable=False)
    status = Column(SQLAlchemyEnum(TransactionStatusEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    participant = relationship("ParticipantModel", back_populates="transactions")