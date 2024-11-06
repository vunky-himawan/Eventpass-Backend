from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

class AttendaceMethodEnum(Enum):
    PIN = "PIN"
    WAJAH = "WAJAH"

class AttendanceStatusEnum(Enum):
    BERHASIL = "BERHASIL"
    GAGAL = "GAGAL"

class AttendanceModel(Base):
    __tablename__ = "attendances"

    attendance_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    receptionist_id = Column(String(36), ForeignKey("event_employees.event_employee_id"), nullable=False)
    participant_id = Column(String(36), ForeignKey("participants.participant_id"), nullable=False)
    ticket_id = Column(String(36), ForeignKey("tickets.ticket_id"), nullable=False)
    attended_in_at = Column(DateTime(timezone=True), nullable=True)
    attended_out_at = Column(DateTime(timezone=True), nullable=True)
    pin = Column(String(6), nullable=False)
    attendance_method = Column(SQLAlchemyEnum(AttendaceMethodEnum), nullable=False)
    status = Column(SQLAlchemyEnum(AttendanceStatusEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    event = relationship("EventModel", back_populates="attendance_tickets")
    receptionist = relationship("ReceptionistModel", back_populates="events")
    participant = relationship("ParticipantModel", back_populates="events")
    ticket = relationship("AttendanceTicketModel", back_populates="events")