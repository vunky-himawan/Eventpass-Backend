from sqlalchemy import String, DateTime, ForeignKey, Text
from ...config.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import uuid

class NotificationModel(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.user_id"), nullable=False
    )
    type: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    for_model: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    data: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    read_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["UserModel"] = relationship('UserModel', uselist=False, back_populates="notifications")

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "type": self.type,
            "for_model": self.for_model,
            "data": self.data,
            "read_at": self.read_at,
            "created_at": self.created_at
        }