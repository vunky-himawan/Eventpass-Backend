import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Enum as SQLAlchemyEnum
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
    refresh_token: Mapped[str] = mapped_column(String(400), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    participant: Mapped["ParticipantModel"] = relationship('ParticipantModel', uselist=False, back_populates="user")
    event_organizer: Mapped["EventOrganizerModel"] = relationship('EventOrganizerModel', uselist=False, back_populates="user")
    notifications: Mapped[List["NotificationModel"]] = relationship('NotificationModel', uselist=True, back_populates="user")
    organization_member: Mapped["OrganizationMemberModel"] = relationship('OrganizationMemberModel', uselist=False, back_populates="users")

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

def add_row(engine, username: str, email: str, password: str, role: str, profile_photo_path: Optional[str]):
    new_row = UserModel(username=username, email=email, password=password, role=role, profile_photo_path=profile_photo_path)
    with Session(engine) as session:
        try:
            session.add(new_row)
            session.commit()
        except Exception as e:
            session.rollback()  # Rolls back if there is an exception
            print(f"Error occurred while adding a new row: {e}")
