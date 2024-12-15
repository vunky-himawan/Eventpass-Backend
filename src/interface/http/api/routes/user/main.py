from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.config.database import get_db

from interface.http.api.schemas.result.success_response import SuccessResponse
from interface.http.api.schemas.result.error_response import ErrorResponse
from domain.usecases.user.get_user_by_username.get_user_by_username_usecase import GetUserByUsernameUseCase
from infrastructure.repositories.user.user_repository_implementation import UserRepositoryImplementation
from domain.usecases.user.get_user_by_user_id.get_user_by_user_id_usecase import GetUserByUserIdUseCase
from domain.usecases.change_password.change_password_usecase import ChangePasswordUseCase
from infrastructure.services.password_service import PasswordService
from infrastructure.services.jwt_token_service import JWTTokenService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from interface.http.api.requests.user.change_password_request import ChangePasswordRequest

router = APIRouter()
bearer_scheme = HTTPBearer()

def get_user_by_username_usecase(
    db: AsyncSession = Depends(get_db)
) -> GetUserByUsernameUseCase:
    user_repository = UserRepositoryImplementation(db)
    
    return GetUserByUsernameUseCase(
        user_repository=user_repository,
    )

def get_user_by_user_id_usecase(
    db: AsyncSession = Depends(get_db)
) -> GetUserByUserIdUseCase:
    user_repository = UserRepositoryImplementation(db)
    
    return GetUserByUserIdUseCase(
        user_repository=user_repository,
    )

@router.get("",responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_user(
    user_id: str = Query(None, description="ID user"), 
    username: str = Query(None, description="Username user"),
    get_user_by_username_usecase: GetUserByUsernameUseCase = Depends(get_user_by_username_usecase),
    get_user_by_user_id_usecase: GetUserByUserIdUseCase = Depends(get_user_by_user_id_usecase)
    ):
    try:
        if user_id is None and username is None:
            return ErrorResponse(message="User ID or username is required", data=None)
        
        if user_id is not None:
            result = await get_user_by_user_id_usecase.call(user_id)

            if result is None:
                return ErrorResponse(message="User not found", data=None)
        
            return SuccessResponse(message="User retrieved successfully", data=result)
        
        if username is not None:
            result = await get_user_by_username_usecase.call(username)

            if result is None:
                return ErrorResponse(message="User not found", data=None)
            
            return SuccessResponse(message="User retrieved successfully", data=result)

    except ValueError as e:
        return ErrorResponse(message="Get user failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Get user failed", data=str(e))
    
def change_password_usecase(
    db: AsyncSession = Depends(get_db)
) -> ChangePasswordUseCase:
    user_repository = UserRepositoryImplementation(db)
    password_service = PasswordService()
    jwt_service = JWTTokenService()
    
    return ChangePasswordUseCase(
        user_repository=user_repository,
        password_service=password_service,
        jwt_service=jwt_service
    )

@router.put("/change-password", responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def change_password(
    request: ChangePasswordRequest,
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    change_password_usecase: ChangePasswordUseCase = Depends(change_password_usecase),
):
    try:
        token = token.credentials

        result = await change_password_usecase.call(token=token, old_password=request.old_password, new_password=request.new_password)

        if result.is_success():
            return SuccessResponse(message="Password changed successfully", data=result.result_value())
        else:
            return ErrorResponse(message="Password change failed", detail=result.error_message())

    except ValueError as e:
        return ErrorResponse(message="Password change failed", data=str(e))
    except Exception as e:
        return ErrorResponse(message="Password change failed", data=str(e))