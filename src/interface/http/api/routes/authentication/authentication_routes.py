from fastapi import APIRouter, Depends
from interface.http.api.schemas.result.success_response import SuccessResponse
from interface.http.api.schemas.result.error_response import ErrorResponse
from interface.http.api.schemas.registration.registration_schema import RegistrationRequest
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.config.database import get_db
from domain.usecases.registration.registration_usecase import RegistrationUseCase
from infrastructure.services.password_service import PasswordService
from infrastructure.repositories.user.user_repository_implementation import UserRepositoryImplementation
from infrastructure.repositories.authentication.authentication_repository_implementation import AuthenticationRepositoryImplementation
from infrastructure.services.image_service import ImageService
from infrastructure.services.face_recognition_service import FaceRecognitionService
from domain.usecases.registration.registration_params import RegistrationParams
from interface.http.api.schemas.login.login_schema import LoginRequest
from domain.usecases.login.login_usecase import LoginUseCase
from infrastructure.services.jwt_token_service import JWTTokenService
from domain.usecases.login.login_params import LoginParams

router = APIRouter()
def get_login_usecase(db: AsyncSession = Depends(get_db)) -> LoginUseCase:
    user_repository = UserRepositoryImplementation(db)
    authentication_repository = AuthenticationRepositoryImplementation(db)
    password_service = PasswordService()
    jwt_service = JWTTokenService()

    return LoginUseCase(
        authentication_repository=authentication_repository,
        jwt_service=jwt_service,
        password_service=password_service,
        user_repository=user_repository
    )
@router.post("/login", 
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def login(request: LoginRequest, login_usecase: LoginUseCase = Depends(get_login_usecase)):
    try:
        params = LoginParams(
            username=request.username,
            password=request.password
        )

        result = await login_usecase.call(params)

        if result.is_success():
            return SuccessResponse(message="Login successful", data=result.result_value())
        else:
            return ErrorResponse(message="Login failed", data=result.error_message())

    except ValueError as e:
        return ErrorResponse(message="Login failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Login failed", data=str(e))



def get_registration_usecase(
    db: AsyncSession = Depends(get_db)
) -> RegistrationUseCase:
    password_service = PasswordService()
    user_repository = UserRepositoryImplementation(db)
    authentication_repository = AuthenticationRepositoryImplementation(db)
    image_service = ImageService(storage_directory='uploads/dataset')
    face_detection_service = FaceRecognitionService()
    
    return RegistrationUseCase(
        password_service=password_service,
        user_repository=user_repository,
        authentication_repository=authentication_repository,
        image_service=image_service,
        face_detection_service=face_detection_service
    )

@router.post(
    "/register",
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
)
async def register(
    registration_request: RegistrationRequest = Depends(RegistrationRequest.as_form),
    registration_usecase: RegistrationUseCase = Depends(get_registration_usecase)
):
    try:
        params = RegistrationParams(
            username=registration_request.username,
            password=registration_request.password,
            email=registration_request.email,
            role=registration_request.role,
            face_photo=registration_request.face_photo,
            details=registration_request.details
        )

        result = await registration_usecase.call(params)

        if result.is_success():
            return SuccessResponse(message="Pendaftaran berhasil", data=result.result_value().to_dict())
        else:
            return ErrorResponse(message="Gagal dalam proses pendaftaran", detail=result.error_message())
        
    except ValueError as e:
        print("ValueError: ", e)
        return ErrorResponse(message="Gagal dalam proses pendaftaran", detail="Terjadi kesalahan")
    except Exception as e:
        print("Exception: ", e)
        return ErrorResponse(message="Gagal dalam proses pendaftaran", detail="Terjadi kesalahan")
    
