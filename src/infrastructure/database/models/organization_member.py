from sqlalchemy import Column, String, ForeignKey
from ...config.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import List

class OrganizationMemberModel(Base):
    __tablename__ = "organization_members"

    organization_member_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.user_id"), nullable=False
    )
    event_organizer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("event_organizers.event_organizer_id"), nullable=False
    )

    users: Mapped[List["UserModel"]] = relationship(
            "UserModel", 
            uselist=False, 
            back_populates="organization_member",
            lazy="selectin",
    )
    event_organizer: Mapped["EventOrganizerModel"] = relationship(
            "EventOrganizerModel",  
            uselist=False, 
            back_populates="organization_member",
            lazy="selectin",
    )
    attendances: Mapped[List["AttendanceModel"]] = relationship(
            "AttendanceModel", 
            uselist=True, 
            back_populates="organization_member",
            lazy="selectin",
    )

    def to_dict(self):
        return {
            "organization_member_id": self.organization_member_id,
            "user_id": self.user_id,
            "event_organizer_id": self.event_organizer_id
        }

    def as_dict(self):
        return {
            "organization_member_id": self.organization_member_id,
            "user_id": self.user_id,
            "event_organizer_id": self.event_organizer_id
        }

    async def as_dict_with_relations_from_organization(self):
        return {
            "organization_member_id": self.organization_member_id,
            "event_organizer_id": self.event_organizer_id,
            "user": await self.user.as_dict_with_relations_from_organization_member(),
        }

    async def as_dict_with_relations(self):
        return {
            "organization_member_id": self.organization_member_id,
            "user_id": self.user_id,
            "event_organizer_id": self.event_organizer_id,
            "user": await self.users.as_dict_with_relations(),
            "event_organizer": await self.event_organizer.as_dict_with_relations(),
        }
