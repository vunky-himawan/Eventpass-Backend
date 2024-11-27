from sqlalchemy import Column, String, ForeignKey
from ...config.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class OrganizationMemberModel(Base):
    __tablename__ = "organization_members"

    organization_member_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.user_id"), nullable=False
    )
    event_organizer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("event_organizers.event_organizer_id"), nullable=False
    )

    event_organizer: Mapped["EventOrganizerModel"] = relationship(
        "EventOrganizerModel", back_populates="organization_members"
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="organization_members")

    # employee: Mapped["EventEmployeeModel"] = relationship("EventEmployeeModel", back_populates="organization_member")
    
    # Ensure proper back_populates in EventModel
    # event: Mapped["EventModel"] = relationship("EventModel", back_populates="organization_members")

