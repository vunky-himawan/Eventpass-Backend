from sqlalchemy import Column, String, DateTime, ForeignKey
from ..config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class TicketModel(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    transaction_id = Column(String(36), ForeignKey("transactions.transaction_id"), nullable=False)
    pin = Column(String(6), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    event = relationship("EventModel", back_populates="tickets")
    transaction = relationship("TransactionModel", back_populates="tickets")