from abc import ABC, abstractmethod
import uuid

class EventRepository(ABC):
    @abstractmethod
    async def get_event(self, event_id:str | uuid.UUID):
        pass

    @abstractmethod
    async def create_event(
        self, 
        title: str, 
        thumbnail_path: str, 
        event_organizer_id: str, 
        address: str, 
        description: str, 
        type: str, 
        status: str, 
        ticket_price: int, 
        ticket_quantity: int, 
        start_date: str
    ):
        pass

    @abstractmethod
    async def update_event(self, event_id: uuid.UUID, **update_data):
        pass

    @abstractmethod
    async def delete_event(self, event_id: uuid.UUID):
        pass

    @abstractmethod
    async def get_event_with_on_going_status_with_receptionist_id(self, receptionist_id: str) -> list[dict]:
        pass