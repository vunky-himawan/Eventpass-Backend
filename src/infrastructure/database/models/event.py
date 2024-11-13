from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SQLAlchemyEnum, DateTime
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
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    event_organizer: Mapped["EventOrganizerModel"] = relationship("EventOrganizerModel", back_populates="events")
