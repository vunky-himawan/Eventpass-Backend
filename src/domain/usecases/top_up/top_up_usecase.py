from domain.repositories.transaction.transaction_repository import TransactionRepository
from infrastructure.services.jwt_token_service import JWTTokenService
from domain.repositories.participant.participant_repository import ParticipantRepository
from domain.repositories.user.user_repository import UserRepository
from domain.entities.result.result import Result, Failed, Success

class TopUpUseCase:
    def __init__(self, 
                 transaction_repository: TransactionRepository, 
                 participant_repository: ParticipantRepository, 
                 user_repository: UserRepository,
                 jwt_service: JWTTokenService):
        self.jwt_service = jwt_service
        self.transaction_repository = transaction_repository
        self.participant_repository = participant_repository
        self.user_repository = user_repository

    async def call(self, token: str) -> Result[dict]:
        try:
            verify_token = self.jwt_service.verify_token(token)

            if not verify_token:
                return Failed(message="Token tidak valid")
            
            result_user = await self.user_repository.get_user_by_user_id(user_id=verify_token["sub"])

            if result_user.is_failed():
                return Failed(message="User tidak valid")
            
            participant_id = result_user.result_value()['details']['participant_id']

            amount = 1000000

            result = await self.transaction_repository.create_transaction(participant_id=participant_id, amount=amount, title="Top Up", category="TOP_UP")

            if not result:
                return Failed(message="Transaksi gagal")
            
            isAddBalance = await self.participant_repository.add_balance(participant_id=participant_id, amount=amount)

            if not isAddBalance:
                return Failed(message="Gagal menambahkan balance")

            return Success(value=result)
        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))