from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class EventOrganizerModel(Base):
    __tablename__ = "event_organizers"

    event_organizer_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.user_id"), nullable=False
    )
    organization_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    address: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    phone_number: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["UserModel"] = relationship(
            "UserModel", 
            uselist=False, 
            back_populates="event_organizer",
            lazy="selectin",
    )
    organization_member: Mapped["OrganizationMemberModel"] = relationship(
            "OrganizationMemberModel", 
            uselist=False, 
            back_populates="event_organizer",
            lazy="selectin",
    )
    events: Mapped[List["EventModel"]] = relationship(
            "EventModel", 
            uselist=True, 
            back_populates="event_organizer",
            lazy="selectin",
    )

    def to_dict(self):
        return {
            "event_organizer_id": self.event_organizer_id,
            "user_id": self.user_id,
            "organization_name": self.organization_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "description": self.description,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def as_dict(self):
        return {
            "event_organizer_id": self.event_organizer_id,
            "organization_name": self.organization_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "description": self.description,
            "amount": self.amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    async def as_dict_with_relations(self):
        return {
            "event_organizer_id": self.event_organizer_id,
            "organization_name": self.organization_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "description": self.description,
            "amount": self.amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": await self.user.as_dict_with_relations_from_organization(),
            "organization_member": await self.organization_member.as_dict_with_relations_from_organization(),
            "events": [await event.as_dict_with_relations_from_organization() for event in self.events]
        }
