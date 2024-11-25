from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 
from infrastructure.config.database import get_db

# Services
from infrastructure.services.face_recognition_service import FaceRecognitionService
from infrastructure.services.image_service import ImageService

# Request
from src.interface.http.api.requests.attendance.attendance_request import AttendanceRequest, FaceAttendanceConfirmationRequest, PinAttendanceConfirmationRequest

# Response
from interface.http.api.schemas.result.success_response import SuccessResponse
from interface.http.api.schemas.result.error_response import ErrorResponse

# Repository Implementation
from infrastructure.repositories.event.main import EventRepositoryImplementation
from infrastructure.repositories.ticket.ticket_repository_implementation import TicketRepositoryImplementation
from infrastructure.repositories.face_recognition.face_recognition_repository_implementation import FaceRecognitionRepositoryImplementation
from infrastructure.repositories.participant.participant_repository_implementation import ParticipantRepositoryImplementation
from infrastructure.repositories.attendance.attendance_repository_implementation import AttendanceRepositoryImplementation
from infrastructure.repositories.transaction.transaction_repository_implementation import TransactionRepositoryImplementation
from infrastructure.repositories.user.user_repository_implementation import UserRepositoryImplementation

# Use Case
from src.domain.usecases.attendance.attendance_usecase import AttendanceUseCase
from domain.usecases.attendance_history.attendance_history_usecase import AttendanceHistoryUseCase
from src.domain.usecases.pin_attendance_confirmation.pin_attendance_confirmation_usecase import PinAttendanceConfirmationUseCase
from src.domain.usecases.face_attendance_confirmation.face_attendance_confirmation_usecase import FaceAttendanceConfirmationUseCase

# Params
from domain.params.attendance.main import FaceAttendanceConfirmationParams, PinAttendanceConfirmationParams
from domain.params.attendance.main import AttendanceParams


router = APIRouter()

def get_attendance_usecase(
    db: AsyncSession = Depends(get_db)
) -> AttendanceUseCase:
    event_repository = EventRepositoryImplementation(db)
    user_repository = UserRepositoryImplementation(db)
    ticket_repository = TicketRepositoryImplementation(db)
    face_recognition_repository = FaceRecognitionRepositoryImplementation(db)
    image_service = ImageService(storage_directory='uploads/dataset')
    face_recognition_service = FaceRecognitionService()
    
    return AttendanceUseCase(
        user_repository=user_repository,
        event_repository=event_repository,
        face_recognition_service=face_recognition_service,
        face_recognition_repository=face_recognition_repository,
        ticket_repository=ticket_repository,
        image_service=image_service
    )


@router.post("/",
             responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
)
async def attendace(
    request: AttendanceRequest = Depends(AttendanceRequest.as_form), 
    attendance_usecase: AttendanceUseCase = Depends(get_attendance_usecase)
):
    try:
        params = AttendanceParams(
            photo=request.photo,
            receptionist_id=request.receptionist_id
        )

        result = await attendance_usecase.call(params)

        if result.is_success():
            return SuccessResponse(message="Prediction successful", data=result.result_value())
        else:
            print(result.error_message())
            return ErrorResponse(message="Prediction failed", detail=result.error_message())

    except ValueError as e:
        return ErrorResponse(message="Prediction failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Prediction failed", data=str(e))
    

def get_face_attendance_confirmation_usecase(
    db: AsyncSession = Depends(get_db)
) -> FaceAttendanceConfirmationUseCase:
    user_repository = UserRepositoryImplementation(db)
    participant_repository = ParticipantRepositoryImplementation(db)
    attendance_repository = AttendanceRepositoryImplementation(db)
    
    return FaceAttendanceConfirmationUseCase(
        user_repository=user_repository,
        participant_repository=participant_repository,
        attendance_repository=attendance_repository
    )

@router.post("/face/confirmation", 
             responses={
                 200: {"model": SuccessResponse},
                 400: {"model": ErrorResponse},
                 500: {"model": ErrorResponse}
    },
)
async def face_attendance_confirmation(
    request: FaceAttendanceConfirmationRequest = Depends(FaceAttendanceConfirmationRequest.as_form),
    attendance_confirmation_usecase: FaceAttendanceConfirmationUseCase = Depends(get_face_attendance_confirmation_usecase)
):
    try:
        params = FaceAttendanceConfirmationParams(
            is_correct=request.is_correct,
            receptionist_id=request.receptionist_id,
            participant_username=request.participant_username,
            event_id=request.event_id
        )
        
        result = await attendance_confirmation_usecase.call(params)

        if result.is_success():
            return SuccessResponse(message="Konfirmasi berhasil", data=result.result_value())
        else:
            return ErrorResponse(message="Konfirmasi gagal", detail=result.error_message())
    
    except Exception as e:
        return ErrorResponse(message="Gagal konfirmasi", data=str(e))
    

def get_pin_attendance_confirmation_usecase(
    db: AsyncSession = Depends(get_db)
) -> PinAttendanceConfirmationUseCase:
    ticket_repository = TicketRepositoryImplementation(db)
    transaction_repository = TransactionRepositoryImplementation(db)
    event_repository = EventRepositoryImplementation(db)
    attendance_repository = AttendanceRepositoryImplementation(db)
    
    return PinAttendanceConfirmationUseCase(
        ticket_repository=ticket_repository,
        event_repository=event_repository,
        transaction_repository=transaction_repository,
        attendance_repository=attendance_repository
    )
    
@router.post("/pin/confirmation",
             responses={
                 200: {"model": SuccessResponse},
                 400: {"model": ErrorResponse},
                 500: {"model": ErrorResponse}
             },
            )
async def pin_attendance_confirmation(
    request: PinAttendanceConfirmationRequest = Depends(PinAttendanceConfirmationRequest.as_form),
    attendance_confirmation_usecase: PinAttendanceConfirmationUseCase = Depends(get_pin_attendance_confirmation_usecase)
):
    try:
        params = PinAttendanceConfirmationParams(
            pin=request.pin,
            receptionist_id=request.receptionist_id
        )

        result = await attendance_confirmation_usecase.call(params)

        if result.is_success():
            return SuccessResponse(message="Konfirmasi berhasil", data=result.result_value())
        else:
            return ErrorResponse(message="Konfirmasi gagal", detail=result.error_message())

    except ValueError as e:
        return ErrorResponse(message="Prediction failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Prediction failed", data=str(e))
    

def get_attendance_repository(
    db: AsyncSession = Depends(get_db)
) -> AttendanceHistoryUseCase:
    attendance_repository = AttendanceRepositoryImplementation(db)
    
    return AttendanceHistoryUseCase(
        attendance_repository=attendance_repository
    )

@router.get("/history/{receptionist_id}",
            responses={
                200: {"model": SuccessResponse},
                400: {"model": ErrorResponse},
                500: {"model": ErrorResponse}
            },
)
async def get_attendance_history(
    receptionist_id: str,
    attendance_history_usecase: AttendanceHistoryUseCase = Depends(get_attendance_repository)
):
    try:
        results = await attendance_history_usecase.call(receptionist_id)

        print("RESULTS: ", results.result_value())

        if results.is_success():
            return SuccessResponse(message="History retrieved successfully", data=results.result_value())
        else:
            return ErrorResponse(message="History not retrieved", detail=results.error_message())

    except ValueError as e:
        print(e)
        return ErrorResponse(message="Get history failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Get history failed", data=str(e))