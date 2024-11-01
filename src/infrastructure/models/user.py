from sqlalchemy import Column, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from ..config.database import Base
import uuid
from enum import Enum

class RoleEnum(Enum):
    EVENT_ORGANIZER = "Event Organizer"
    PARTICIPANT = "Participant"
    SUPERADMIN = "Superadmin"
    RECEPTIONIST = "Receptionist"

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(SQLAlchemyEnum(RoleEnum), nullable=False)
    profile_photo_path = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())