from abc import ABC, abstractmethod
from typing import Optional, Union
import uuid

from src.infrastructure.database.models.event import EventModel

class EventRepository(ABC):
    @abstractmethod
    async def get_all_by_title_or_type_or_status(self, title_or_type: str):
        pass
    
    @abstractmethod
    async def get_count_all(self):
        pass

    @abstractmethod
    async def get_all(self, current_page: int = 1, page_size: int = 10):
        pass

    @abstractmethod
    async def get_event(self, event_id:str | uuid.UUID)-> Union[EventModel, None]:
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
        start_date: str,
        receptionist_1: uuid.UUID,
        receptionist_2: Optional[uuid.UUID],
    ) -> Union[EventModel, None]:
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

    @abstractmethod
    async def substract_ticket(self, event_id: uuid.UUID) -> bool:
        pass

    @abstractmethod
    async def get_upcoming_events(self, current_page: int, page_size: int) -> list[dict]:
        pass