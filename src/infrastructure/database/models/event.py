import re
from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SQLAlchemyEnum, DateTime
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from typing import List

class EventStatusEnum(enum.Enum):
    BUKA = "BUKA"
    TUTUP = "TUTUP"
    BERLANGSUNG = "BERLANGSUNG"
    SELESAI = "SELESAI"

class EventTypeEnum(enum.Enum):
    SEMINAR = "SEMINAR"
    KONVERENSI = "KONVERENSI"
    WORKSHOP = "WORKSHOP"
    FESTIVAL = "FESTIVAL"
    LAINNYA = "LAINNYA"
    EXPO = "EXPO"

class EventModel(Base):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    event_organizer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("event_organizers.event_organizer_id"), nullable=False
    )
    thumbnail_path: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[EventTypeEnum] = mapped_column(SQLAlchemyEnum(EventTypeEnum), nullable=False)
    status: Mapped[EventStatusEnum] = mapped_column(SQLAlchemyEnum(EventStatusEnum), nullable=False)
    ticket_price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ticket_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    receptionist_1: Mapped[str] = mapped_column(
            String(36), ForeignKey("organization_members.organization_member_id"), nullable=False
    )
    receptionist_2: Mapped[str] = mapped_column(
            String(36), ForeignKey("organization_members.organization_member_id"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tickets: Mapped[List["TicketModel"]] = relationship('TicketModel', uselist=True, back_populates="event")
    feedback_ratings: Mapped[List["FeedbackRatingModel"]] = relationship(
            'FeedbackRatingModel', 
            uselist=True, 
            back_populates="event",
            lazy="selectin"
    )
    event_organizer: Mapped["EventOrganizerModel"] = relationship(
            'EventOrganizerModel', 
            uselist=False, 
            back_populates="events",
            lazy="selectin"
    )
    attendances: Mapped[List["AttendanceModel"]] = relationship('AttendanceModel', uselist=True, back_populates="event")
    event_speakers: Mapped[List["EventSpeakerModel"]] = relationship(
            'EventSpeakerModel', 
            uselist=True, 
            back_populates="event",
            lazy="selectin",
            cascade="all, delete-orphan"
    )

    class Config:
        orm_mode = True

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_organizer_id": self.event_organizer_id,
            "thumbnail_path": self.thumbnail_path,
            "title": self.title,
            "address": self.address,
            "description": self.description,
            "type": self.type.name,
            "status": self.status.name,
            "ticket_price": self.ticket_price,
            "ticket_quantity": self.ticket_quantity,
            "start_date": self.start_date,
            "receptionist_1": self.receptionist_1,
            "receptionist_2": self.receptionist_2,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def as_dict(self):
        return {
            "event_id": self.event_id,
            "event_organizer_id": self.event_organizer_id,
            "thumbnail_path": self.thumbnail_path,
            "title": self.title,
            "address": self.address,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "ticket_price": self.ticket_price,
            "ticket_quantity": self.ticket_quantity,
            "start_date": self.start_date,
            "receptionist_1": self.receptionist_1,
            "receptionist_2": self.receptionist_2,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    async def as_dict_with_relations_from_organization(self):
        return {
            "event_id": self.event_id,
            "event_organizer_id": self.event_organizer_id,
            "thumbnail_path": self.thumbnail_path,
            "title": self.title,
            "address": self.address,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "ticket_price": self.ticket_price,
            "ticket_quantity": self.ticket_quantity,
            "start_date": self.start_date,
            "receptionist_1": self.receptionist_1,
            "receptionist_2": self.receptionist_2,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "event_speakers": [await event_speaker.as_dict_with_relations() for event_speaker in self.event_speakers],
            "feedback_ratings": [await feedback_rating.as_dict_with_relations() for feedback_rating in self.feedback_ratings],
        }

    async def as_dict_with_relations(self):
        return {
            "event_id": self.event_id,
            "event_organizer_id": self.event_organizer_id,
            "thumbnail_path": self.thumbnail_path,
            "title": self.title,
            "address": self.address,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "ticket_price": self.ticket_price,
            "ticket_quantity": self.ticket_quantity,
            "start_date": self.start_date,
            "receptionist_1": self.receptionist_1,
            "receptionist_2": self.receptionist_2,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "event_organizer": self.event_organizer.as_dict(),
            "event_speakers": [await event_speaker.as_dict_with_relations() for event_speaker in self.event_speakers],
            "feedback_ratings": [await feedback_rating.as_dict_with_relations() for feedback_rating in self.feedback_ratings],
        }
