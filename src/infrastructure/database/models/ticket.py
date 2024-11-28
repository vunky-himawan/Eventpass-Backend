from sqlalchemy import String, DateTime, ForeignKey
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TicketModel(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.event_id"), nullable=False
    )
    transaction_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("transactions.transaction_id"), nullable=False
    )
    pin: Mapped[str] = mapped_column(
        String(6), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    event: Mapped["EventModel"] = relationship('EventModel', uselist=False, back_populates="tickets")
    transaction: Mapped["TransactionModel"] = relationship('TransactionModel', uselist=False, back_populates="ticket", lazy="joined")

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "event_id": self.event_id,
            "transaction_id": self.transaction_id,
            "pin": self.pin,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }