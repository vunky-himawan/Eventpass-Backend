from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLAlchemyEnum, UniqueConstraint
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

    participant: Mapped["ParticipantModel"] = relationship(
            'ParticipantModel', 
            uselist=False, 
            back_populates="attendances",
            lazy="selectin"
    )
    event: Mapped["EventModel"] = relationship(
            'EventModel', 
            uselist=False, 
            back_populates="attendances",
            lazy="selectin"
    )
    organization_member: Mapped["OrganizationMemberModel"] = relationship(
            'OrganizationMemberModel', 
            uselist=False, 
            back_populates="attendances",
            lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint('event_id', 'participant_id', 'attendance_method', 'status', name='unique_event_participant_method_status'),
    )

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

    def as_dict(self):
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

    
    async def as_dict_with_relations_from_participant(self):
        return {
            "attendance_id": self.attendance_id,
            "event_id": self.event_id,
            "receptionist_id": self.receptionist_id,
            "participant_id": self.participant_id,
            "attended_in_at": self.attended_in_at,
            "attendance_method": self.attendance_method,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "event": await self.event.as_dict_with_relations(),
            "organization_member": await self.organization_member.as_dict_with_relations(),
        }

    async def as_dict_with_relations(self):
        return {
            "attendance_id": self.attendance_id,
            "event_id": self.event_id,
            "receptionist_id": self.receptionist_id,
            "participant_id": self.participant_id,
            "attended_in_at": self.attended_in_at,
            "attendance_method": self.attendance_method,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "participant": await self.participant.as_dict_with_relations(),
            "event": await self.event.as_dict_with_relations(),
            "organization_member": await self.organization_member.as_dict_with_relations(),
        }
    
    def to_dict_with_participant(self):
        return {
            "attendance_id": self.attendance_id,
            "event_id": self.event_id,
            "receptionist_id": self.receptionist_id,
            "participant_id": self.participant_id,
            "attended_in_at": self.attended_in_at,
            "attendance_method": self.attendance_method,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "participant": self.participant.to_dict()
        }
        
