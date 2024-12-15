from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from interface.http.api.schemas.result.error_response import ErrorResponse
from interface.http.api.schemas.result.success_response import SuccessResponse
from infrastructure.config.database import get_db
from infrastructure.repositories.transaction.transaction_repository_implementation import TransactionRepositoryImplementation
from domain.usecases.top_up.top_up_usecase import TopUpUseCase
from infrastructure.repositories.participant.participant_repository_implementation import ParticipantRepositoryImplementation
from infrastructure.repositories.user.user_repository_implementation import UserRepositoryImplementation
from infrastructure.services.jwt_token_service import JWTTokenService
from fastapi import HTTPException
from domain.usecases.get_transactions.get_transactions_usecase import GetTransactionsUseCase

router = APIRouter()

bearer_security = HTTPBearer()

def get_transactions_usecase(
    db: AsyncSession = Depends(get_db)
) -> GetTransactionsUseCase:
    transaction_repository = TransactionRepositoryImplementation(db)
    user_repository = UserRepositoryImplementation(db)
    jwt_service = JWTTokenService()
    
    return GetTransactionsUseCase(
        transaction_repository=transaction_repository,
        user_repository=user_repository,
        jwt_service=jwt_service
    )
@router.get('',
             responses={
                 200: {"model": SuccessResponse},
                 400: {"model": ErrorResponse},
                 500: {"model": ErrorResponse}
             })
async def get_transactions(
    token: HTTPAuthorizationCredentials = Depends(bearer_security),
    get_transactions_use_case: GetTransactionsUseCase = Depends(get_transactions_usecase)
):
    try:
        result = await get_transactions_use_case.call(token=token.credentials)

        if result.is_success():
            return SuccessResponse(message="Get transactions successful", data=result.result_value())
        else:
            return ErrorResponse(message="Get transactions failed", detail=result.error_message())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def top_up_usecase(
    db: AsyncSession = Depends(get_db)
) -> TopUpUseCase:
    transaction_repository = TransactionRepositoryImplementation(db)
    participant_repository = ParticipantRepositoryImplementation(db)
    user_repository = UserRepositoryImplementation(db)
    jwt_service = JWTTokenService()
    
    return TopUpUseCase(
        transaction_repository=transaction_repository,
        participant_repository=participant_repository,
        user_repository=user_repository,
        jwt_service=jwt_service
    )
@router.post('/top-up',
             responses={
                 200: {"model": SuccessResponse},
                 400: {"model": ErrorResponse},
                 500: {"model": ErrorResponse}
             })
async def top_up(
    token: HTTPAuthorizationCredentials = Depends(bearer_security),
    top_up_use_case: TopUpUseCase = Depends(top_up_usecase)
):
    try:
        result = await top_up_use_case.call(token=token.credentials)

        if result.is_success():
            return SuccessResponse(message="Top up successful", data=result.result_value())
        else:
            return ErrorResponse(message="Top up failed", detail=result.error_message())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))