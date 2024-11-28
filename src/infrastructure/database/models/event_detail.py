# from sqlalchemy import String, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from ...config.database import Base
# import uuid

# class EventDetailModel(Base):
#     __tablename__ = "event_details"

#     event_detail_id: Mapped[str] = mapped_column(
#         String(36), primary_key=True, default=lambda: str(uuid.uuid4())
#     )
#     event_id: Mapped[str] = mapped_column(
#         String(36), ForeignKey("events.event_id"), nullable=False
#     )
#     event_receiptionist_id: Mapped[str] = mapped_column(
#         String(36), ForeignKey("event_employees.event_employee_id"), nullable=False
#     )
#     speaker_id: Mapped[str] = mapped_column(
#         String(36), ForeignKey("speakers.speaker_id"), nullable=False
#     )

#     event_employee: Mapped["EventEmployeeModel"] = relationship('EventEmployeeModel', uselist=False, back_populates="event_details")

#     def as_dict(self):
#         return {
#             "event_detail_id": self.event_detail_id,
#             # "event_id": self.event,
#             "event_receiptionist": self.event_receiptionist,
#             "speaker": self.speaker
#         }

