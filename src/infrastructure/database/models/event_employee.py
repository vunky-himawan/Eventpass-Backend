from sqlalchemy import Column, String, ForeignKey
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

    organization_member: Mapped["OrganizationMemberModel"] = relationship(
        "OrganizationMemberModel", back_populates="event_employees"
    )
