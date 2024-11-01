from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from ..config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class NotificationModel(Base):
    __tablename__ = "notifications"

    notification_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    type = Column(String(255), nullable=False)
    for_model = Column(Text, nullable=False)
    data = Column(Text, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="notifications")