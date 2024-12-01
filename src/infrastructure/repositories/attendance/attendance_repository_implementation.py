from typing import List
from domain.repositories.attendance.attendance_repository import AttendanceRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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
            if await self.check_attendance_exists(event_id, participant_id, attended_method, status):
                raise ValueError("Pengunjung sudah melakukan absensi")

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

            return attendance

        except ValueError as e:
            print(f"Error creating attendance: {e}")
            raise e
        except Exception as e:
            print(f"Error creating attendance: {e}")
            raise e
        
    async def get_attendance_history_by_receptionist_id(self, receptionist_id: str) -> List[dict]:
        try:
            query = select(AttendanceModel).where(AttendanceModel.receptionist_id == receptionist_id)
            execution_result = await self.db.execute(query)
            results = execution_result.scalars().all()
            
            attendances = []

            for result in results:
                attendance = result.to_dict_with_participant()

                attendances.append(attendance)

            return attendances

        except ValueError as e:
            print(f"Error getting attendance history: {e}")
            raise e
        except Exception as e:
            print(f"Error getting attendance history: {e}")
            raise e
        
    async def check_attendance_exists(self, event_id: str, participant_id: str, method: AttendaceMethodEnum, status: AttendanceStatusEnum) -> bool:
        try:
            query = select(AttendanceModel).where(AttendanceModel.event_id == event_id, AttendanceModel.participant_id == participant_id, AttendanceModel.attendance_method == method, AttendanceModel.status == status)
            execution_result = await self.db.execute(query)
            results = execution_result.scalars().all()
            
            if len(results) > 0:
                return True
            else:
                return False

        except ValueError as e:
            print(f"Error checking attendance exists: {e}")
            raise e
        except Exception as e:
            print(f"Error checking attendance exists: {e}")
            raise e