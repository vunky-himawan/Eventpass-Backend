from domain.entities.result.result import Result, Failed, Success
from domain.repositories.participant.participant_repository import ParticipantRepository
from domain.repositories.user.user_repository import UserRepository
from domain.params.attendance.main import FaceAttendanceConfirmationParams
from domain.repositories.attendance.attendance_repository import AttendanceRepository
from infrastructure.database.models.attendance import AttendaceMethodEnum, AttendanceStatusEnum

class FaceAttendanceConfirmationUseCase:
    def __init__(self, 
                 participant_repository: ParticipantRepository,
                 user_repository: UserRepository,
                 attendance_repository: AttendanceRepository,
                 ):
        self.participant_repository = participant_repository
        self.user_repository = user_repository
        self.attendance_repository = attendance_repository
        

    async def call(self, params: FaceAttendanceConfirmationParams) -> Result[dict]:
        try:
            attendance = await self.attendance_repository.create_attendance(
                event_id=params.event_id,
                receptionist_id=params.receptionist_id,
                participant_id=params.participant_id,
                attended_method=AttendaceMethodEnum.WAJAH.value,
                status=AttendanceStatusEnum.BERHASIL.value if params.is_correct else AttendanceStatusEnum.GAGAL.value
            )

            return Success(value=attendance.to_dict())

        except ValueError as e:
            print(f"Error creating attendance: {e}")
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))