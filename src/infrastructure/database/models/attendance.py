from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from ...config.database import Base
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

class AttendaceMethodEnum(Enum):
    PIN = "PIN"
    WAJAH = "WAJAH"

class AttendanceStatusEnum(Enum):
    BERHASIL = "BERHASIL"
    GAGAL = "GAGAL"

class AttendanceModel(Base):
    __tablename__ = "attendances"

    attendance_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id: Mapped[str] = mapped_column(String(36), ForeignKey("events.event_id"), nullable=False)
    receptionist_id: Mapped[str] = mapped_column(String(36), ForeignKey("event_employees.event_employee_id"), nullable=False)
    participant_id: Mapped[str] = mapped_column(String(36), ForeignKey("participants.participant_id"), nullable=False)
    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("tickets.ticket_id"), nullable=False)
    attended_in_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    attended_out_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    pin: Mapped[str] = mapped_column(String(6), nullable=False)
    attendance_method: Mapped[AttendaceMethodEnum] = mapped_column(SQLAlchemyEnum(AttendaceMethodEnum), nullable=False)
    status: Mapped[AttendanceStatusEnum] = mapped_column(SQLAlchemyEnum(AttendanceStatusEnum), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    event: Mapped["EventModel"] = relationship("EventModel", back_populates="attendance_tickets")
    receptionist: Mapped["ReceptionistModel"] = relationship("ReceptionistModel", back_populates="events")
    participant: Mapped["ParticipantModel"] = relationship("ParticipantModel", back_populates="events")
    ticket: Mapped["AttendanceTicketModel"] = relationship("AttendanceTicketModel", back_populates="events")
