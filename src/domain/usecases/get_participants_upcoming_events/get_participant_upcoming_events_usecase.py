from domain.repositories.event_participant.event_participant_repository import EventParticipantRepository
from domain.repositories.user.user_repository import UserRepository
from domain.entities.result.result import Result, Failed, Success
from infrastructure.services.jwt_token_service import JWTTokenService
from domain.entities.user.user import User
from typing import List

class GetParticipantUpcomingEventsUseCase:
    def __init__(self, 
                 event_participant_repository: EventParticipantRepository,
                 user_repository: UserRepository,
                 jwt_service: JWTTokenService):
         self.user_repository = user_repository
         self.jwt_service = jwt_service
         self.event_participant_repository = event_participant_repository

    async def call(self, token: str) -> Result[List[dict]]:
        try:
            verify_token = self.jwt_service.verify_token(token)

            if not verify_token:
                return Failed(message="Access token tidak valid")
            
            user_id = verify_token['sub']

            result = await self.user_repository.get_user_by_user_id(user_id)

            if result.is_failed():
                return Failed(message="User tidak ditemukan")
            
            user_detail = result.result_value()

            upcoming_participant_events = await self.event_participant_repository.get_upcoming_participant_events(participant_id=user_detail['details']['participant_id'])

            if upcoming_participant_events is None:
                return Failed(message="Upcoming participant events not found")
            
            if len(upcoming_participant_events) == 0:
                return Success(value=[])
            
            events = []

            print("upcoming_participant_events", upcoming_participant_events)

            for event in upcoming_participant_events:
                events.append(event['event'])

            return Success(value=events)

        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))