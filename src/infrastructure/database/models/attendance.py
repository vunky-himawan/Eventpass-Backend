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
    receptionist_id: Mapped[str] = mapped_column(String(36), ForeignKey("organization_members.organization_member_id"), nullable=False)
    participant_id: Mapped[str] = mapped_column(String(36), ForeignKey("participants.participant_id"), nullable=False)
    attended_in_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    attendance_method: Mapped[AttendaceMethodEnum] = mapped_column(SQLAlchemyEnum(AttendaceMethodEnum), nullable=False)
    status: Mapped[AttendanceStatusEnum] = mapped_column(SQLAlchemyEnum(AttendanceStatusEnum), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    participant: Mapped["ParticipantModel"] = relationship('ParticipantModel', uselist=False, back_populates="attendances")
    event: Mapped["EventModel"] = relationship('EventModel', uselist=False, back_populates="attendances")
    organization_member: Mapped["OrganizationMemberModel"] = relationship('OrganizationMemberModel', uselist=False, back_populates="attendances")

    def to_dict(self):
        return {
            "attendance_id": self.attendance_id,
            "event_id": self.event_id,
            "receptionist_id": self.receptionist_id,
            "participant_id": self.participant_id,
            "attended_in_at": self.attended_in_at,
            "attendance_method": self.attendance_method,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }