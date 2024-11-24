from sqlalchemy import Column, String, ForeignKey, desc

from infrastructure.database.models.event_detail import EventDetailModel

from ...config.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

class EventEmployeeModel(Base):
    __tablename__ = "event_employees"

    event_employee_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    organization_member_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organization_members.organization_member_id"), nullable=False
    )

    # organization_member: Mapped["OrganizationMemberModel"] = relationship(
    #     "OrganizationMemberModel", back_populates="event_employees"
    # )
    # event: Mapped["EventModel"] = relationship("EventModel", back_populates="employee")

    organization_member: Mapped["OrganizationMemberModel"] = relationship(
        "OrganizationMemberModel", 
        back_populates="employee",
        lazy="joined",
    )
    # event_details: Mapped["EventDetailModel"] = relationship(
    #         "EventDetailModel", 
    #         back_populates="employee", 
    #         cascade="all, delete-orphan"
    # )

    def as_dict(self):
        return {
            "event_employee_id": self.event_employee_id,
            "organization_member_id": self.organization_member_id,
            # "organization_member": self.organization_member,
            # "event": self.event,
        }

