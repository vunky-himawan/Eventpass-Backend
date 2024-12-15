from abc import ABC, abstractmethod
import uuid

class TicketRepository(ABC):
    @abstractmethod
    async def create_ticket(self, event_id: str | uuid.UUID, participant_id: str | uuid.UUID) -> dict:
        pass

    @abstractmethod
    async def get_tickets_by_event_id(self, event_id: str | uuid.UUID) -> list[dict]:
        pass

    @abstractmethod
    async def get_ticket_by_pin(self, pin: str) -> dict:
        pass