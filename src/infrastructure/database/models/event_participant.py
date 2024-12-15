from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.sql import func
from ...config.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class EventParticipantModel(Base):
    __tablename__ = "event_participants"

    event_participant_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    participant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("participants.participant_id"), nullable=False
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.event_id"), nullable=False
    )
    ticket_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tickets.ticket_id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    participant: Mapped["ParticipantModel"] = relationship(
            "ParticipantModel", 
            uselist=False, 
            back_populates="event_participant",
            lazy="selectin",
    )
    event: Mapped["EventModel"] = relationship(
            "EventModel", 
            uselist=False, 
            back_populates="event_participants",
            lazy="selectin",
    )
    ticket: Mapped["TicketModel"] = relationship(
            "TicketModel", 
            uselist=False, 
            back_populates="event_participant",
            lazy="selectin",
    )

    def to_dict(self):
        return {
            "event_participant_id": self.event_participant_id,
            "participant_id": self.participant_id,
            "event_id": self.event_id,
            "ticket_id": self.ticket_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def to_dict_with_event(self):
        return {
            "event_participant_id": self.event_participant_id,
            "participant_id": self.participant_id,
            "event_id": self.event_id,
            "ticket_id": self.ticket_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "event": self.event.to_dict(),
        }
    
    def to_dict_with_relations(self):
        return {
            "event_participant_id": self.event_participant_id,
            "participant_id": self.participant_id,
            "event_id": self.event_id,
            "ticket_id": self.ticket_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "participant": self.participant.to_dict(),
            "event": self.event.to_dict(),
            "ticket": self.ticket.to_dict(),
        }