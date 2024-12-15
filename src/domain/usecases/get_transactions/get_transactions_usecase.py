from domain.repositories.transaction.transaction_repository import TransactionRepository
from domain.entities.result.result import Result, Failed, Success
from domain.repositories.user.user_repository import UserRepository
from infrastructure.services.jwt_token_service import JWTTokenService

class GetTransactionsUseCase:
    def __init__(self, 
                 transaction_repository: TransactionRepository, 
                 user_repository: UserRepository,
                 jwt_service: JWTTokenService):
        self.jwt_service = jwt_service
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    async def call(self, token: str) -> Result[dict]:
        try:
            verify_token = self.jwt_service.verify_token(token)

            result = await self.user_repository.get_user_by_user_id(user_id=verify_token['sub'])

            user = result.result_value()

            print(user['details']['participant_id'])

            transactions = await self.transaction_repository.get_transactions_by_participant_id(participant_id=user['details']['participant_id'])

            if not transactions:
                return Failed(message="No transactions found")
            
            return Success(value=transactions)

        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))
