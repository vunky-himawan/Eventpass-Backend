from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum as SQLAlchemyEnum, DateTime
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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

    event_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_organizer_id = Column(String(36), ForeignKey("event_organizers.event_organizer_id"), nullable=False)
    thumbnail_path = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(SQLAlchemyEnum(EventTypeEnum), nullable=False)
    status = Column(SQLAlchemyEnum(EventStatusEnum), nullable=False)
    ticket_price = Column(Integer, nullable=False, default=0)
    ticket_quantity = Column(Integer, nullable=False, default=0)
    start_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    event_organizer = relationship("EventOrganizerModel", back_populates="events")