from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from infrastructure.repositories.event.main import EventRepositoryImplementation
from infrastructure.repositories.organization_member.organization_member_repository_implementation import OrganizationMemberRepositoryImplementation
from domain.usecases.logout.logout_usecase import LogoutUseCase
from interface.http.api.requests.auth.logout_request import LogoutRequest
from domain.usecases.get_logged_in_user.get_logged_in_user import GetLoggedInUserUseCase
from src.interface.http.api.requests.auth.refresh_token_request import RefreshTokenRequest
from domain.usecases.refresh_token.refresh_token_usecase import RefreshTokenUseCase
from infrastructure.services.jwt_token_service import JWTTokenService

router = APIRouter()
bearer_scheme = HTTPBearer()

def get_login_usecase(db: AsyncSession = Depends(get_db)) -> LoginUseCase:
    user_repository = UserRepositoryImplementation(db)
    event_repository = EventRepositoryImplementation(db)
    organization_member_repository = OrganizationMemberRepositoryImplementation(db)
    authentication_repository = AuthenticationRepositoryImplementation(db)
    password_service = PasswordService()
    jwt_service = JWTTokenService()

    return LoginUseCase(
        authentication_repository=authentication_repository,
        event_repository=event_repository,
        organization_member_repository=organization_member_repository,
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
            print(result.error_message())
            return ErrorResponse(message="Login failed", detail=result.error_message())

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
    face_recognition_service = FaceRecognitionService()
    
    return RegistrationUseCase(
        password_service=password_service,
        user_repository=user_repository,
        authentication_repository=authentication_repository,
        image_service=image_service,
        face_recignition_service=face_recognition_service
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
            role=registration_request.role.value,
            face_photo=registration_request.face_photo,
            details=registration_request.details
        )

        result = await registration_usecase.call(params)

        if result.is_success():
            return SuccessResponse(message="Pendaftaran berhasil", data=result.result_value().to_dict())
        else:
            print(result.error_message())
            return ErrorResponse(message="Gagal dalam proses pendaftaran", detail=result.error_message())
        
    except ValueError as e:
        return ErrorResponse(message="Gagal dalam proses pendaftaran", detail="Terjadi kesalahan")
    except Exception as e:
        return ErrorResponse(message="Gagal dalam proses pendaftaran", detail="Terjadi kesalahan")
    

def get_logout_usecase(
    db: AsyncSession = Depends(get_db)
) -> LogoutUseCase:
    user_repository = UserRepositoryImplementation(db)
    jwt_service = JWTTokenService()
    
    return LogoutUseCase(
        jwt_service=jwt_service,
        user_repository=user_repository
    )

@router.post(
    "/logout",
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
)
async def logout(
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    logout_usecase: LogoutUseCase = Depends(get_logout_usecase)
):
    try:
        token = authorization.credentials

        result = await logout_usecase.call(token=token)

        print(result)

        if result.is_success():
            return SuccessResponse(message="Logout berhasil", data=result.result_value())
        else:
            print(result.error_message())
            return ErrorResponse(message="Logout gagal", detail=result.error_message())

    except ValueError as e:
        print(e)
        return ErrorResponse(message="Logout gagal", data=str(e))
    except Exception as e:
        print(e)
        return ErrorResponse(message="Logout gagal", data=str(e))
    
def get_get_logged_in_user_usecase(
    db: AsyncSession = Depends(get_db)
) -> GetLoggedInUserUseCase:
    authentication_repository = AuthenticationRepositoryImplementation(db)
    jwt_service = JWTTokenService()
    
    return GetLoggedInUserUseCase(
        authentication_repository=authentication_repository,
        jwt_service=jwt_service
    )

@router.get(
    "/get_logged_in_user",
    dependencies=[Depends(bearer_scheme)],
    openapi_extra={
        "description": "Get the currently logged-in user. Requires Authorization header with a Bearer token.",
        "example": "Authorization: Bearer <token>"
    },
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_logged_in_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    get_logged_in_user_usecase: GetLoggedInUserUseCase = Depends(get_get_logged_in_user_usecase)
): 
    try:
        token = token.credentials

        result = await get_logged_in_user_usecase.call(token=token)

        if result.is_success():
            return SuccessResponse(message="Get logged in user successful", data=result.result_value())
        else:
            return ErrorResponse(message="Get logged in user failed", detail=result.error_message())

    except ValueError as e:
        return ErrorResponse(message="Get logged in user failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Get logged in user failed", data=str(e))
    

def get_refresh_token_usecase(
    db: AsyncSession = Depends(get_db)
) -> RefreshTokenUseCase:
    user_repository = UserRepositoryImplementation(db)
    authentication_repository = AuthenticationRepositoryImplementation(db)
    jwt_service = JWTTokenService()
    
    return RefreshTokenUseCase(
        user_repository=user_repository,
        authentication_repository=authentication_repository,
        jwt_service=jwt_service
    )

@router.post(
    "/refresh",
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def refresh_token(
    request: RefreshTokenRequest,
    refresh_token_usecase: RefreshTokenUseCase = Depends(get_refresh_token_usecase)
):
    try:
        result = await refresh_token_usecase.call(refresh_token=request.refresh_token)

        if result.is_success():
            return SuccessResponse(message="Refresh token successful", data=result.result_value())
        else:
            return ErrorResponse(message="Refresh token failed", detail=result.error_message())

    except ValueError as e:
        return ErrorResponse(message="Refresh token failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Refresh token failed", data=str(e))