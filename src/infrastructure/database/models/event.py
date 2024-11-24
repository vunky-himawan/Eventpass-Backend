import re
from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SQLAlchemyEnum, DateTime

from infrastructure.database.models.event_detail import EventDetailModel
from infrastructure.database.models.event_employee import EventEmployeeModel
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

class EventStatusEnum(enum.Enum):
    BUKA = "BUKA"
    TUTUP = "TUTUP"
    SELESAI = "SELESAI"

class EventTypeEnum(enum.Enum):
    SEMINAR = "SEMINAR"
    KONVERENSI = "KONFERENSI"
    WORKSHOP = "WORKSHOP"
    FESTIVAL = "FESTIVAL"
    LAINNYA = "LAINNYA"
    EXPO = "EXPO"
    KONVENSI = "KONVENSI"

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

    # organizer: Mapped["EventOrganizerModel"] = relationship("EventOrganizerModel", back_populates="events")
    # employee: Mapped["EventEmployeeModel"] = relationship("EventEmployeeModel", back_populates="event")
    
    organizer: Mapped["EventOrganizerModel"] = relationship(
            "EventOrganizerModel", 
            back_populates="events",
            lazy="selectin",
    )
    event_details: Mapped["EventDetailModel"] = relationship(
            "EventDetailModel", 
            back_populates="event", 
            cascade="all, delete-orphan",
            lazy="selectin",
    )
    employees: Mapped["EventEmployeeModel"] = relationship(
            "EventEmployeeModel",
            back_populates="event",
            lazy="selectin",
    )
    # organization_members: Mapped["OrganizationMemberModel"] = relationship("OrganizationMemberModel", back_populates="event")

    def as_dict(self):
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
        }
    
    def as_dict_with_detail(self):
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
                "details": self.event_details.as_dict() if self.event_details else None
        }
