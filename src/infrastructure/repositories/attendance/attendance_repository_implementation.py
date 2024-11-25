from typing import Any, Coroutine
from domain.repositories.attendance.attendance_repository import AttendanceRepository
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.attendance.attendance import Attendance
from src.infrastructure.database.models.attendance import AttendaceMethodEnum, AttendanceStatusEnum, AttendanceModel
from datetime import datetime

class AttendanceRepositoryImplementation(AttendanceRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_attendance(self, event_id: str, 
                                receptionist_id: str, 
                                participant_id: str, 
                                attended_method: AttendaceMethodEnum, 
                                status: AttendanceStatusEnum) -> Attendance:
        try:
            attendance = AttendanceModel(
                event_id=event_id,
                receptionist_id=receptionist_id,
                participant_id=participant_id,
                attended_in_at=datetime.now(),
                attendance_method=attended_method,
                status=status
            )

            self.db.add(attendance)
            await self.db.commit()
            await self.db.refresh(attendance)

            attendance = Attendance(
                event_attendance_id=attendance.attendance_id,
                event_id=attendance.event_id,
                receptionist_id=attendance.receptionist_id,
                participant_id=attendance.participant_id,
                attended_in_at=attendance.attended_in_at,
                attendance_method=attendance.attendance_method,
                status=attendance.status,
                created_at=attendance.created_at,
                updated_at=attendance.updated_at
            )

            print("Attendance created successfully ", attendance)

            return attendance

        except ValueError as e:
            print(f"Error creating attendance: {e}")
            raise e
        except Exception as e:
            print(f"Error creating attendance: {e}")
            raise e