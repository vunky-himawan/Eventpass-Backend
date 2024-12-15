from domain.entities.result.result import Result, Failed, Success
from domain.repositories.event_participant.event_participant_repository import EventParticipantRepository
from infrastructure.services.jwt_token_service import JWTTokenService
from domain.repositories.user.user_repository import UserRepository

class CheckIsPurchasedUseCase:
    def __init__(self,
                 event_participant_repository: EventParticipantRepository,
                 user_repository: UserRepository,
                 jwt_service: JWTTokenService,
                 ):
        self.jwt_service = jwt_service
        self.user_repository = user_repository
        self.event_participant_repository = event_participant_repository
    
    async def call(self, event_id: str, token: str) -> Result[dict]:
        try:
            verify_token = self.jwt_service.verify_token(token)

            if not verify_token:
                return Failed(message="Token tidak valid")
            
            result_user = await self.user_repository.get_user_by_user_id(user_id=verify_token["sub"])

            if result_user.is_failed():
                return Failed(message="User tidak valid")
            
            participant_id = result_user.result_value()['details']['participant_id']
            
            result = await self.event_participant_repository.check_is_purchased(event_id=event_id, participant_id=participant_id)

            if result.is_failed():
                return Success(value={
                    'isPurchased': False,
                    'ticket': None,
                    'event': None,
                })
            
            details = result.result_value()

            response = {
                'isPurchased': True,
                'ticket': details['ticket'],
                'event': details['event'],
            }

            return Success(value=response)
        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))