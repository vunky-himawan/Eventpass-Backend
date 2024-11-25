# from sqlalchemy import Column, String, ForeignKey, desc

# from ...config.database import Base
# import uuid
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from typing import List

# class EventEmployeeModel(Base):
#     __tablename__ = "event_employees"

#     event_employee_id: Mapped[str] = mapped_column(
#         String(36), primary_key=True, default=lambda: str(uuid.uuid4())
#     )
#     organization_member_id: Mapped[str] = mapped_column(
#         String(36), ForeignKey("organization_members.organization_member_id"), nullable=False
#     )

#     event_details: Mapped[List["EventDetailModel"]] = relationship('EventDetailModel', uselist=True, back_populates="event_employee")