from sqlalchemy import SmallInteger, String, ForeignKey, Enum as SQLAlchemyEnum, Integer, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from ...config.database import Base
import enum
from typing import List

class Gender(str, enum.Enum): 
    LAKI_LAKI = "LAKI_LAKI"
    PEREMPUAN = "PEREMPUAN"

class ParticipantModel(Base):
    __tablename__ = "participants"

    participant_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.user_id"), nullable=False
    )
    participant_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    age: Mapped[int] = mapped_column(
        SmallInteger, nullable=False
    )
    gender: Mapped[Gender] = mapped_column(
        SQLAlchemyEnum(Gender), nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    birth_date: Mapped[Date] = mapped_column(
        Date, nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["UserModel"] = relationship('UserModel', uselist=False, back_populates="participant")
    transactions: Mapped[List["TransactionModel"]] = relationship(
            'TransactionModel', 
            uselist=True, 
            back_populates="participant",
            lazy="selectin"
    )
    feedback_ratings: Mapped[List["FeedbackRatingModel"]] = relationship(
            'FeedbackRatingModel', 
            uselist=True, 
            back_populates="participant",
            lazy="selectin"
    )
    face_photos: Mapped[List["FacePhotoModel"]] = relationship(
            'FacePhotoModel', 
            uselist=True, 
            back_populates="participant",
            lazy="selectin"
    )
    attendances: Mapped[List["AttendanceModel"]] = relationship(
            'AttendanceModel', 
            uselist=True, 
            back_populates="participant",
            lazy="selectin"
    )

    def to_dict(self):
        return {
            "participant_id": self.participant_id,
            "user_id": self.user_id,
            "participant_name": self.participant_name,
            "age": self.age,
            "gender": self.gender.name,
            "amount": self.amount,
            "birth_date": self.birth_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def as_dict(self):
        return {
            "participant_id": self.participant_id,
            "user_id": self.user_id,
            "participant_name": self.participant_name,
            "age": self.age,
            "gender": self.gender,
            "amount": self.amount,
            "birth_date": self.birth_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    async def as_dict_with_relations_from_feedback_ratings(self):
        return {
            "participant_id": self.participant_id,
            "user_id": self.user_id,
            "participant_name": self.participant_name,
            "age": self.age,
            "gender": self.gender,
            "amount": self.amount,
            "birth_date": self.birth_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": self.user.as_dict(),
            "transactions": [await transaction.as_dict_with_relations_from_participant() for transaction in self.transactions],
            "attendances": [await attendance.as_dict_with_relations_from_participant() for attendance in self.attendances],
        }
    
    async def as_dict_with_relations(self):
        return {
            "participant_id": self.participant_id,
            "user_id": self.user_id,
            "participant_name": self.participant_name,
            "age": self.age,
            "gender": self.gender,
            "amount": self.amount,
            "birth_date": self.birth_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": self.user.as_dict(),
            "transactions": [await transaction.as_dict_with_relations() for transaction in self.transactions],
            "feedback_ratings": [await feedback_rating.as_dict_with_relations() for feedback_rating in self.feedback_ratings],
            "attendances": [await attendance.as_dict_with_relations() for attendance in self.attendances],
        }
