from abc import ABC, abstractmethod
from typing import List
from domain.entities.result.result import Result

class EventParticipantRepository(ABC):
    @abstractmethod
    async def create_event_participant(self, participant_id: str, event_id: str, ticket_id: str) -> bool:
        pass

    @abstractmethod
    async def get_upcoming_participant_events(self, participant_id: str) -> List[dict]:
        pass

    @abstractmethod
    async def check_is_purchased(self, event_id: str, participant_id: str) -> Result[dict]:
        pass