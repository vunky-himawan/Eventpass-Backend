from sqlalchemy import String, DateTime, ForeignKey, Integer, Enum as SQLAlchemyEnum
from ...config.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    transaction_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    participant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("participants.participant_id"), nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    category: Mapped[TransactionCategoryEnum] = mapped_column(
        SQLAlchemyEnum(TransactionCategoryEnum), nullable=False
    )
    status: Mapped[TransactionStatusEnum] = mapped_column(
        SQLAlchemyEnum(TransactionStatusEnum), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    participant: Mapped["ParticipantModel"] = relationship(
        "ParticipantModel", back_populates="transactions"
    )
