from abc import ABC, abstractmethod
from domain.entities.result.result import Result
import uuid

class EventOrganizerRepository(ABC):
    @abstractmethod
    async def get_event_organizer_by_event_organizer_id(self, event_organizer_id: str) -> Result[dict]:
        pass

    @abstractmethod
    async def subtract_balance(self, event_organizer_id: str | uuid.UUID, amount: int) -> bool:
        pass

    @abstractmethod
    async def add_balance(self, event_organizer_id: str | uuid.UUID, amount: int) -> bool:
        pass