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
            'ParticipantModel', 
            uselist=False, 
            back_populates="transactions",
            lazy="selectin"
    )
    ticket: Mapped["TicketModel"] = relationship(
            'TicketModel', 
            uselist=False, 
            back_populates="transaction",
            lazy="selectin"
    )

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "participant_id": self.participant_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category.name,
            "status": self.status.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def as_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "participant_id": self.participant_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    async def as_dict_with_relations_from_participant(self):
        return {
            "transaction_id": self.transaction_id,
            "participant_id": self.participant_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    async def as_dict_with_relations(self):
        return {
            "transaction_id": self.transaction_id,
            "participant_id": self.participant_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "participant": await self.participant.as_dict_with_relations(),
            "ticket": await self.ticket.as_dict_with_relations(),
        }
