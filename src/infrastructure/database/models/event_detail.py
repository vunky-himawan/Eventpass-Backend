from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ...config.database import Base
import uuid

class EventDetailModel(Base):
    __tablename__ = "event_details"

    event_detail_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    event_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("events.event_id"), nullable=False
    )
    event_receiptionist_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("event_employees.event_employee_id"), nullable=False
    )
    speaker_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("speakers.speaker_id"), nullable=False
    )
