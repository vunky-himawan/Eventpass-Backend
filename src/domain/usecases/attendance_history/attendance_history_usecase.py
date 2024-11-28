from domain.repositories.attendance.attendance_repository import AttendanceRepository
from domain.entities.attendance.attendance import Attendance
from typing import List
from domain.entities.result.result import Result, Failed, Success

class AttendanceHistoryUseCase:
    def __init__(self, attendance_repository: AttendanceRepository):
        self.attendance_repository = attendance_repository

    async def call(self, receptionist_id: str) -> Result[List[dict]]:
        try:
            results = await self.attendance_repository.get_attendance_history_by_receptionist_id(receptionist_id=receptionist_id)

            if results is None:
                return Failed(message="Attendance not found")
            
            print(results)
            
            return Success(value=results)

        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))