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
            result = await self.user_repository.get_user_by_username(username=params.participant_username)

            if result.is_failed():
                return Failed(message=result.error_message())
            
            user = result.result_value()

            participant = await self.participant_repository.get_participant_by_user_id(user_id=user["user_id"])

            if participant is None:
                return Failed(message="Participant not found")
            
            attendance = await self.attendance_repository.create_attendance(
                event_id=params.event_id,
                receptionist_id=params.receptionist_id,
                participant_id=participant.participant_id,
                attended_method=AttendaceMethodEnum.WAJAH.value,
                status=AttendanceStatusEnum.BERHASIL.value if params.is_correct else AttendanceStatusEnum.GAGAL.value
            )

            return Success(value=attendance.to_dict())

        except Exception as e:
            return Failed(message=str(e))