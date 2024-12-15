import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Enum as SQLAlchemyEnum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from ...config.database import Base
import uuid
from enum import Enum
from typing import List

class RoleEnum(Enum):
    EVENT_ORGANIZER = "EVENT_ORGANIZER"
    PARTICIPANT = "PARTICIPANT"
    SUPERADMIN = "SUPERADMIN"
    RECEPTIONIST = "RECEPTIONIST"

class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(SQLAlchemyEnum(RoleEnum), nullable=True)
    profile_photo_path: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    participant: Mapped["ParticipantModel"] = relationship('ParticipantModel', uselist=False, back_populates="user", lazy="joined")
    event_organizer: Mapped["EventOrganizerModel"] = relationship('EventOrganizerModel', uselist=False, back_populates="user", lazy="joined")
    notifications: Mapped[List["NotificationModel"]] = relationship('NotificationModel', uselist=True, back_populates="user")
    organization_member: Mapped["OrganizationMemberModel"] = relationship('OrganizationMemberModel', uselist=True, back_populates="users", lazy="joined")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "role": self.role,
            "profile_photo": self.profile_photo_path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def user_to_dict_with_details(self, with_password: bool | None = None):
        details = None
        
        if self.role == RoleEnum.PARTICIPANT:
            details = self.participant.to_dict()
        elif self.role == RoleEnum.EVENT_ORGANIZER:
            details = self.event_organizer.to_dict()
        elif self.role == RoleEnum.RECEPTIONIST:
            details = self.organization_member.to_dict()

        result = {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "role": self.role,
            "profile_photo": self.profile_photo_path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "details": details
        }

        if with_password:
            result["password"] = self.password

        return result

    async def as_dict_with_relations_from_organization(self):
        return {
            "username": self.username,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "role": self.role,
            "profile_photo": self.profile_photo_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "notifications": [await notification.as_dict_with_relations() for notification in self.notifications],
        }

    async def as_dict_with_relations_from_organization_member(self):
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "profile_photo": self.profile_photo_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    async def as_dict_with_relations(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "role": self.role,
            "profile_photo": self.profile_photo_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "participant": await self.participant.as_dict_with_relations(),
            "event_organizer": await self.event_organizer.as_dict_with_relations(),
            "notifications": [await notification.as_dict_with_relations() for notification in self.notifications],
            "organization_member": [await organization_member.as_dict_with_relations() for organization_member in self.organization_member],
        }

