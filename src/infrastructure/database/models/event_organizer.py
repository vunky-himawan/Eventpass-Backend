from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
        "UserModel", back_populates="event_organizer"
    )
