from abc import ABC, abstractmethod
from infrastructure.database.models.attendance import AttendaceMethodEnum, AttendanceStatusEnum
from domain.entities.attendance.attendance import Attendance
from typing import List

class AttendanceRepository(ABC):
    @abstractmethod
    async def create_attendance(self,
                                event_id: str,
                                receptionist_id: str,
                                participant_id: str,
                                attended_method: AttendaceMethodEnum,
                                status: AttendanceStatusEnum) -> Attendance:
        pass

    @abstractmethod
    async def get_attendance_history_by_receptionist_id(self, receptionist_id: str) -> List[dict]:
        pass

    @abstractmethod
    async def check_attendance_exists(self, event_id: str, participant_id: str, method: AttendaceMethodEnum, status: AttendanceStatusEnum) -> bool:
        pass