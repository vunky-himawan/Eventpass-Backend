from domain.repositories.event.main import EventRepository
from domain.repositories.event_participant.event_participant_repository import EventParticipantRepository
from domain.repositories.participant.participant_repository import ParticipantRepository
from domain.entities.result.result import Result, Failed, Success
from domain.entities.event.event import Event
from domain.entities.participant.participant import Participant
import uuid
from typing import List

class GetParticipantEventsUseCase:
    def __init__(self,
                 event_repository: EventRepository,
                 event_participant_repository: EventParticipantRepository,
                 participant_repository: ParticipantRepository):
        self.event_repository = event_repository
        self.event_participant_repository = event_participant_repository
        self.participant_repository = participant_repository

    async def call(self, participant_id: str | uuid.UUID) -> Result[List[dict]]:
        try:
            events = await self.event_repository.get_upcoming_events(current_page=1, page_size=10)
        except ValueError as e:
            return Failed(message=str(e))
        except Exception as e:
            return Failed(message=str(e))
