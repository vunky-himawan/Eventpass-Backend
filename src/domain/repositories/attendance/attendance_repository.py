from abc import ABC, abstractmethod
from infrastructure.database.models.attendance import AttendaceMethodEnum, AttendanceStatusEnum
from domain.entities.attendance.attendance import Attendance

class AttendanceRepository(ABC):
    @abstractmethod
    async def create_attendance(self,
                                event_id: str,
                                receptionist_id: str,
                                participant_id: str,
                                attended_method: AttendaceMethodEnum,
                                status: AttendanceStatusEnum) -> Attendance:
        pass