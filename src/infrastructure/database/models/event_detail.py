from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
        String(36), ForeignKey("organization_members.organization_member_id"), nullable=False
    )

    event: Mapped["EventModel"] = relationship(
            "EventModel", 
            back_populates="event_details",
            lazy="joined",
    )
    event_receiptionist: Mapped["OrganizationMemberModel"] = relationship(
            "OrganizationMemberModel", 
            back_populates="event_details",
            lazy="joined",
    )
    employee: Mapped["EventEmployeeModel"] = relationship(
            "EventEmployeeModel", 
            back_populates="event_details",
            primaryjoin="EventDetailModel.event_detail_id == EventEmployeeModel.event_detail_id",
            lazy="joined",
    )

    def as_dict(self):
        return {
            "event_detail_id": self.event_detail_id,
            # "event_id": self.event,
            "event_receiptionist": self.event_receiptionist,
            "speaker": self.speaker
        }

