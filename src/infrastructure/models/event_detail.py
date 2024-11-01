from sqlalchemy import Column, String, Text, Integer, ForeignKey
from ..config.database import Base
import uuid

class EventDetailModel(Base):
    __tablename__ = "event_details"

    event_detail_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    event_receiptionist_id = Column(String(36), ForeignKey("event_employees.event_employee_id"), nullable=False)
    speaker_id = Column(String(36), ForeignKey("speakers.speaker_id"), nullable=False)
